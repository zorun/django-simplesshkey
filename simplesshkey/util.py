# -*- coding: utf-8 -*-

# Copyright (c) 2017, Baptiste Jonglez
# Copyright (c) 2014-2016, Clemson University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of Clemson University nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import unicode_literals

from . import settings

import base64
import binascii
import struct


def wrap(text, width, wrap_end=None):
    n = 0
    t = ""
    if wrap_end is None:
        while n < len(text):
            m = n + width
            t += text[n:m]
            if len(text) <= m:
                return t
            t += "\n"
            n = m
    else:
        while n < len(text):
            m = n + width
            if len(text) <= m:
                return t + text[n:m]
            m -= len(wrap_end)
            t += text[n:m] + wrap_end + "\n"
            n = m
    return t


def bytes2int(b):
    h = binascii.hexlify(b)
    return int(h, 16)


def int2bytes(i):
    h = "%x" % i
    if len(h) & 1:
        h = "0" + h
    return bytearray.fromhex(h)


class PublicKeyParseError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return "Unrecognized public key format"


class PublicKey(object):
    def __init__(self, b64key, comment=None):
        self.b64key = b64key
        self.comment = comment
        try:
            keydata = base64.b64decode(b64key.encode("ascii"))
        except binascii.Error as e:  # Python 3 raises this instead of TypeError
            raise TypeError(str(e))
        self.keydata = keydata
        self.parts = []
        while keydata:
            dlen = struct.unpack(">I", keydata[:4])[0]
            data, keydata = keydata[4:(4+dlen)], keydata[(4+dlen):]
            self.parts.append(data)
        try:
            self.algorithm = self.parts[0].decode("ascii")
        except UnicodeDecodeError as e:
            raise TypeError(str(e))

    def keytype(self):
        return self.algorithm

    def fingerprint(self, hash=None):
        import hashlib

        if hash is None:
            hash = settings.SSHKEY_DEFAULT_HASH
        if hash in ("md5", "legacy"):
            fp = hashlib.md5(self.keydata).hexdigest()
            fp = ":".join(a + b for a, b in zip(fp[::2], fp[1::2]))
            if hash == "md5":
                return "MD5:" + fp
            else:
                return fp
        elif hash == "sha256":
            fp = hashlib.sha256(self.keydata).digest()
            fp = base64.b64encode(fp).decode("ascii").rstrip("=")
            return "SHA256:" + fp
        else:
            raise ValueError("Unknown hash type: %s" % hash)

    def format_openssh(self):
        out = self.algorithm + " " + self.b64key
        if self.comment:
            out += " " + self.comment
        return out

    def format_rfc4716(self):
        out = "---- BEGIN SSH2 PUBLIC KEY ----\n"
        if self.comment:
            comment = 'Comment: "%s"' % self.comment
            out += wrap(comment, 72, "\\") + "\n"
        out += wrap(self.b64key, 72) + "\n"
        out += "---- END SSH2 PUBLIC KEY ----"
        return out

    def format_pem(self):
        if self.algorithm != "ssh-rsa" and len(self.parts) == 3:
            raise TypeError("key is not a valid RSA key")
        from pyasn1.codec.der import encoder as der_encoder
        from pyasn1.type import univ

        e = bytes2int(self.parts[1])
        n = bytes2int(self.parts[2])
        pkcs1_seq = univ.Sequence()
        pkcs1_seq.setComponentByPosition(0, univ.Integer(n))
        pkcs1_seq.setComponentByPosition(1, univ.Integer(e))
        der = der_encoder.encode(pkcs1_seq)
        out = (
            "-----BEGIN RSA PUBLIC KEY-----\n"
            + wrap(base64.b64encode(der).decode("ascii"), 64)
            + "\n"
            + "-----END RSA PUBLIC KEY-----"
        )
        return out


def pubkey_parse_openssh(text):
    fields = text.split(None, 2)
    if len(fields) < 2:
        raise PublicKeyParseError(text)
    try:
        if len(fields) == 2:
            key = PublicKey(fields[1])
        else:
            key = PublicKey(fields[1], fields[2])
    except TypeError:
        raise PublicKeyParseError(text)
    if fields[0] != key.algorithm:
        raise PublicKeyParseError(text)
    return key


def pubkey_parse_rfc4716(text):
    lines = text.splitlines()
    if not (
        lines[0] == "---- BEGIN SSH2 PUBLIC KEY ----"
        and lines[-1] == "---- END SSH2 PUBLIC KEY ----"
    ):
        raise PublicKeyParseError(text)
    lines = lines[1:-1]
    b64key = ""
    headers = {}
    while lines:
        line = lines.pop(0)
        if ":" in line:
            while line[-1] == "\\":
                line = line[:-1] + lines.pop(0)
            k, v = line.split(":", 1)
            headers[k.lower()] = v.lstrip()
        else:
            b64key += line
    comment = headers.get("comment")
    if comment and comment[0] in ('"', "'") and comment[0] == comment[-1]:
        comment = comment[1:-1]
    try:
        return PublicKey(b64key, comment)
    except TypeError:
        raise PublicKeyParseError(text)


def pubkey_parse_pem(text):
    from pyasn1.codec.der import decoder as der_decoder

    lines = text.splitlines()
    if not (
        lines[0] == "-----BEGIN RSA PUBLIC KEY-----"
        and lines[-1] == "-----END RSA PUBLIC KEY-----"
    ):
        raise PublicKeyParseError(text)
    der = base64.b64decode("".join(lines[1:-1]).encode("ascii"))
    pkcs1_seq = der_decoder.decode(der)
    n_val = pkcs1_seq[0][0]
    e_val = pkcs1_seq[0][1]
    n = int2bytes(n_val)
    e = int2bytes(e_val)
    if n[0] & 0x80:
        n = b"\x00" + n
    if e[0] & 0x80:
        e = b"\x00" + e
    algorithm = "ssh-rsa".encode("ascii")
    keydata = (
        struct.pack(">I", len(algorithm))
        + algorithm
        + struct.pack(">I", len(e))
        + e
        + struct.pack(">I", len(n))
        + n
    )
    b64key = base64.b64encode(keydata).decode("ascii")
    return PublicKey(b64key)


def pubkey_parse(text):
    lines = text.splitlines()

    if len(lines) == 1:
        return pubkey_parse_openssh(text)

    if lines[0] == "---- BEGIN SSH2 PUBLIC KEY ----":
        return pubkey_parse_rfc4716(text)

    if lines[0] == "-----BEGIN RSA PUBLIC KEY-----":
        return pubkey_parse_pem(text)

    raise PublicKeyParseError(text)

# encoding: utf8

import poplib
import imaplib
import smtplib
from email import parser, message_from_string
from email.header import decode_header

from utils import log


def connect(host, username, password):
    log("login with '%s' to '%s'" % (username, host))
    pop_conn = poplib.POP3(host)
    pop_conn.user(username)
    pop_conn.pass_(password)
    return pop_conn


def _get_all(pop_conn, as_message=True):
    """
    Get all mail content from the mail server.
    Return the format in message if 'as_message' is True,
    otherwise return the original mime format.
    """
    count, total_size = pop_conn.stat()
    if as_message:
        return [get_message_from_mime(pop_conn.retr(i)) for i in range(1, count+1)]
    else:
        return [pop_conn.retr(i) for i in range(1, count+1)]


def get_all_mimes(pop_conn):
    """
    Get all mail content in the Mime format from mail server.
    """
    return _get_all(pop_conn, False)


def get_all_messages(pop_conn):
    """
    Get all mail content in the Message object format from mail server.
    """
    return _get_all(pop_conn)


def get_message_from_mime(mime):
    """
    Parse an orginal Mime format into a Message object model.
    """
    return message_from_string('\n'.join([line.decode('utf-8') for line in mime[1]]))


def get_subject_from_message(message):
    subject, encode_str = decode_header(message['subject'])[0]
    return subject.decode(encode_str)


if __name__ == '__main__':
    pass

#!/usr/bin/env python
# pylint: disable=line-too-long
"""
Test data for Sate API calls used for mocking in unit tests
"""
TESTDATA = {
    'http://192.168.8.100:5003/api/v1.0/state':'{"state":"000"}',
    'http://192.168.8.100:5003/api/v1.0/state/000':'{"state":"000"}',
    'http://192.168.8.100:5003/api/v1.0/state/001':'{"state":"001"}',
    'http://192.168.8.101:5003/api/v1.0/state':'{"state":"001"}',
    'http://192.168.8.101:5003/api/v1.0/state/001':'{"state":"001"}',
    'http://192.168.8.101:5003/api/v1.0/state/002':'{"state":"002"}',
    'http://192.168.8.102:5003/api/v1.0/state':'{"state":"002"}',
    'http://192.168.8.102:5003/api/v1.0/state/002':'{"state":"002"}',
    'http://192.168.8.102:5003/api/v1.0/state/010':'{"state":"010"}',
    'http://192.168.8.102:5003/api/v1.0/state/001':'{"state":"001"}',
    'http://192.168.8.103:5003/api/v1.0/state':'{"state":"010"}',
    'http://192.168.8.103:5003/api/v1.0/state/010':'{"state":"010"}',
    'http://192.168.8.103:5003/api/v1.0/state/000':'{"state":"000"}',
    'http://192.168.8.103:5003/api/v1.0/state/001':'{"state":"001"}',
}

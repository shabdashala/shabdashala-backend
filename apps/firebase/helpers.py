# -*- coding:utf-8 -*-
from django.conf import settings

import requests

from . import errors as firebase_errors

FIREBASE_API_URL = getattr(settings, "FIREBASE_API_URL", None)

DOMAIN_URL_PREFIX = getattr(
    settings, "FIREBASE_DEEP_LINKS_DOMAIN_URL_PREFIX", None)
ANDROID_PACKAGE_NAME = getattr(
    settings, "FIREBASE_DEEP_LINKS_ANDROID_PACKAGE_NAME", None)
ANDROID_MIN_PACKAGE_VERSION_CODE = getattr(
    settings, "FIREBASE_DEEP_LINKS_ANDROID_MIN_PACKAGE_VERSION_CODE", None)

IOS_BUNDLE_IDENTIFIER = getattr(
    settings, "FIREBASE_DEEP_LINKS_IOS_BUNDLE_IDENTIFIER", None)
IOS_APP_STORE_ID = getattr(
    settings, "FIREBASE_DEEP_LINKS_IOS_APP_STORE_ID", None)
IOS_CUSTOM_SCHEME = getattr(
    settings, "FIREBASE_DEEP_LINKS_IOS_CUSTOM_SCHEME", None)


def generate_dynamic_link_params(link, short=True):
    return {
        "dynamicLinkInfo": {
            "domainUriPrefix": DOMAIN_URL_PREFIX,
            "link": link,
            "androidInfo": {
                "androidPackageName": ANDROID_PACKAGE_NAME,
                # "androidFallbackLink": string,
                # "androidMinPackageVersionCode":
                #     ANDROID_MIN_PACKAGE_VERSION_CODE,
            },
            "iosInfo": {
                "iosBundleId": IOS_BUNDLE_IDENTIFIER,
                # "iosFallbackLink": string,
                # "iosCustomScheme": "twb://",
                # "iosIpadFallbackLink": string,
                # "iosIpadBundleId": string,
                "iosAppStoreId": IOS_APP_STORE_ID
            },
            "navigationInfo": {
                "enableForcedRedirect": '1',
            },
        },
        "suffix": {
            "option": "SHORT" if short else "UNGUESSABLE"
        }
    }


def make_firebase_request(payload, timeout=10, raise_exception=True):
    if not (
        FIREBASE_API_URL
        and DOMAIN_URL_PREFIX
        and ANDROID_PACKAGE_NAME
        and IOS_BUNDLE_IDENTIFIER
        and IOS_APP_STORE_ID
    ):
        raise firebase_errors.FirebaseDynamicLinksInvalidConfigurationError()
    response = requests.post(
        FIREBASE_API_URL, json=payload, timeout=timeout)
    data = response.json()
    if not response.ok:
        if raise_exception:
            raise firebase_errors.FirebaseDynamicLinksError(data)
        else:
            return ""
    return data['shortLink']


def create_firebase_dynamic_link(link, raise_exception=True):
    return make_firebase_request(
        generate_dynamic_link_params(link),
        raise_exception=raise_exception)

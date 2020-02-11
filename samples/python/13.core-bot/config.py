#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    # LUIS_APP_ID = os.environ.get("LuisAppId", "")
    LUIS_APP_ID = "7234a55b-9b3b-4069-9246-6ed6c4847307"
    # LUIS_API_KEY = os.environ.get("LuisAPIKey", "")
    LUIS_API_KEY = "372692912d9f422cafa3e1606b148820"
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    # LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "")
    LUIS_API_HOST_NAME = "westus.api.cognitive.microsoft.com"

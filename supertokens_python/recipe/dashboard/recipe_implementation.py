# Copyright (c) 2021, VRAI Labs and/or its affiliates. All rights reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License") as published by the Apache Software Foundation.
#
# You may not use this file except in compliance with the License. You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from supertokens_python.constants import DASHBOARD_VERSION
from supertokens_python.framework import BaseRequest
from supertokens_python.normalised_url_path import NormalisedURLPath

from .interfaces import RecipeInterface
from .utils import DashboardConfig

if TYPE_CHECKING:
    from supertokens_python.querier import Querier


class RecipeImplementation(RecipeInterface):
    def __init__(self, querier: Querier):
        super().__init__()
        self.querier = querier

    async def get_dashboard_bundle_location(self, user_context: Dict[str, Any]) -> str:
        return f"https://cdn.jsdelivr.net/gh/supertokens/dashboard@v{DASHBOARD_VERSION}/build/"

    async def should_allow_access(
        self,
        request: BaseRequest,
        config: DashboardConfig,
        user_context: Dict[str, Any],
    ) -> bool:
        api_key_header_value = request.get_header("authorization")

        # We receive the api key as `Bearer API_KEY`, this retrieves just the key
        api_key = api_key_header_value.split(
            " ")[1] if api_key_header_value else None

        if api_key is None:
            return False

        return api_key == config.api_key

    async def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        data = {"email": email, "password": password}
        response = await self.querier.send_post_request(NormalisedURLPath("/recipe/dashboard/signin"), data)
        return response

    async def verify(self, sessionId: str) -> Dict[str, Any]:
        data = {"sessionId": sessionId}
        response = await self.querier.send_post_request(NormalisedURLPath('/recipe/dashboard/session/verify'), data)
        return response

    async def sign_out(self, sessionId: str) -> Dict[str, Any]:
        response = await self.querier.send_delete_request(NormalisedURLPath("/recipe/dashboard/session"), {"sessionId": sessionId})
        return response

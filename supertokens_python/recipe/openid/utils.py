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

from typing import TYPE_CHECKING, Callable, Union, Any, Awaitable, Optional

if TYPE_CHECKING:
    from .interfaces import RecipeInterface, APIInterface
    from supertokens_python import AppInfo
    from supertokens_python.recipe.jwt import OverrideConfig as JWTOverrideConfig
    from supertokens_python.framework import BaseRequest

from supertokens_python.normalised_url_domain import NormalisedURLDomain
from supertokens_python.normalised_url_path import NormalisedURLPath


class InputOverrideConfig:
    def __init__(
        self,
        functions: Union[Callable[[RecipeInterface], RecipeInterface], None] = None,
        apis: Union[Callable[[APIInterface], APIInterface], None] = None,
        jwt_feature: Union[JWTOverrideConfig, None] = None,
    ):
        self.functions = functions
        self.apis = apis
        self.jwt_feature = jwt_feature


class OverrideConfig:
    def __init__(
        self,
        functions: Union[Callable[[RecipeInterface], RecipeInterface], None] = None,
        apis: Union[Callable[[APIInterface], APIInterface], None] = None,
    ):
        self.functions = functions
        self.apis = apis


class OpenIdConfig:
    def __init__(
        self,
        override: OverrideConfig,
        issuer_domain: Callable[[BaseRequest, Any], Awaitable[NormalisedURLDomain]],
        issuer_path: NormalisedURLPath,
        is_issuer_domain_given: bool,
    ):
        self.override = override
        self.issuer_domain = issuer_domain
        self.issuer_path = issuer_path
        self.is_issuer_domain_given = is_issuer_domain_given


def validate_and_normalise_user_input(
    app_info: AppInfo,
    issuer: Union[str, None] = None,
    override: Union[InputOverrideConfig, None] = None,
):
    async def issuer_domain(req: BaseRequest, user_context: Any):
        if issuer is None:
            api_domain = await app_info.api_domain(req, user_context)
            return api_domain
        return NormalisedURLDomain(issuer)

    is_issuer_domain_given = issuer is not None

    if issuer is None:
        issuer_path = app_info.api_base_path
    else:
        issuer_path = NormalisedURLPath(issuer)

    if not issuer_path.equals(app_info.api_base_path):
        raise Exception(
            "The path of the issuer URL must be equal to the apiBasePath. The default value is /auth"
        )

    if override is not None and not isinstance(override, InputOverrideConfig):  # type: ignore
        raise ValueError("override must be an instance of InputOverrideConfig or None")

    if override is None:
        override = InputOverrideConfig()

    return OpenIdConfig(
        OverrideConfig(functions=override.functions, apis=override.apis),
        issuer_domain,
        issuer_path,
        is_issuer_domain_given,
    )


async def get_issuer_domain_or_throw_error(
    issuer_domain: Optional[str],
    config: OpenIdConfig,
    app_info: AppInfo,
    user_context: Any,
) -> str:
    if issuer_domain is not None:
        return issuer_domain
    if config.is_issuer_domain_given:
        issuer_domain_resp = await config.issuer_domain(None, user_context)  # type: ignore
        return issuer_domain_resp.get_as_string_dangerous()
    if app_info.initial_api_domain_type == "string":
        issuer_domain_resp = await config.issuer_domain(None, user_context)  # type: ignore
        return issuer_domain_resp.get_as_string_dangerous()
    raise Exception(
        "Please pass issuer_domain as a string to the function or initiate issuer_domain with openid recipe or pass api_domain as string in supertokens.init"
    )

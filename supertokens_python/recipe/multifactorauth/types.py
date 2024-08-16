# Copyright (c) 2024, VRAI Labs and/or its affiliates. All rights reserved.
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

from typing import Awaitable, Dict, Any, Union, List, Optional, Callable

from supertokens_python.recipe.multitenancy.interfaces import TenantConfig
from .interfaces import RecipeInterface, APIInterface
from typing_extensions import Literal
from supertokens_python.types import AccountLinkingUser, RecipeUserId


class MFARequirementList(List[Union[Dict[str, List[str]], str]]):
    def __init__(
        self,
        *args: Union[
            str, Dict[Union[Literal["oneOf"], Literal["allOfInAnyOrder"]], List[str]]
        ]
    ):
        super().__init__()
        for arg in args:
            if isinstance(arg, str):
                self.append(arg)
            else:
                if "oneOf" in arg:
                    self.append({"oneOf": arg["oneOf"]})
                elif "allOfInAnyOrder" in arg:
                    self.append({"allOfInAnyOrder": arg["allOfInAnyOrder"]})
                else:
                    raise ValueError("Invalid dictionary format")


class MFAClaimValue:
    c: Dict[str, Any]
    v: bool

    def __init__(self, c: Dict[str, Any], v: bool):
        self.c = c
        self.v = v


class OverrideConfig:
    def __init__(
        self,
        functions: Union[Callable[[RecipeInterface], RecipeInterface], None] = None,
        apis: Union[Callable[[APIInterface], APIInterface], None] = None,
    ):
        self.functions = functions
        self.apis = apis


class MultiFactorAuthConfig:
    def __init__(
        self,
        first_factors: Optional[List[str]],
        override: OverrideConfig,
    ):
        self.first_factors = first_factors
        self.override = override


class FactorIds:
    EMAILPASSWORD: Literal["emailpassword"] = "emailpassword"
    OTP_EMAIL: Literal["otp-email"] = "otp-email"
    OTP_PHONE: Literal["otp-phone"] = "otp-phone"
    LINK_EMAIL: Literal["link-email"] = "link-email"
    LINK_PHONE: Literal["link-phone"] = "link-phone"
    THIRDPARTY: Literal["thirdparty"] = "thirdparty"
    TOTP: Literal["totp"] = "totp"


class FactorIdsAndType:
    def __init__(
        self,
        factor_ids: List[str],
        type: Union[Literal["string"], Literal["oneOf"], Literal["allOfInAnyOrder"]],
    ):
        self.factor_ids = factor_ids
        self.type = type


class GetFactorsSetupForUserFromOtherRecipesFunc:
    def __init__(
        self,
        func: Callable[[AccountLinkingUser, Dict[str, Any]], Awaitable[List[str]]],
    ):
        self.func = func


class GetAllAvailableSecondaryFactorIdsFromOtherRecipesFunc:
    def __init__(
        self,
        func: Callable[[TenantConfig], Awaitable[List[str]]],
    ):
        self.func = func


class GetEmailsForFactorOkResult:
    status: Literal["OK"] = "OK"

    def __init__(self, factor_id_to_emails_map: Dict[str, List[str]]):
        self.factor_id_to_emails_map = factor_id_to_emails_map


class GetEmailsForFactorUnknownSessionRecipeUserIdResult:
    status: Literal["UNKNOWN_SESSION_RECIPE_USER_ID"] = "UNKNOWN_SESSION_RECIPE_USER_ID"


class GetEmailsForFactorFromOtherRecipesFunc:
    def __init__(
        self,
        func: Callable[
            [AccountLinkingUser, RecipeUserId],
            Awaitable[
                Union[
                    GetEmailsForFactorOkResult,
                    GetEmailsForFactorUnknownSessionRecipeUserIdResult,
                ]
            ],
        ],
    ):
        self.func = func


class GetPhoneNumbersForFactorsOkResult:
    status: Literal["OK"] = "OK"

    def __init__(self, factor_id_to_phone_number_map: Dict[str, List[str]]):
        self.factor_id_to_phone_number_map = factor_id_to_phone_number_map


class GetPhoneNumbersForFactorsUnknownSessionRecipeUserIdResult:
    status: Literal["UNKNOWN_SESSION_RECIPE_USER_ID"] = "UNKNOWN_SESSION_RECIPE_USER_ID"


class GetPhoneNumbersForFactorsFromOtherRecipesFunc:
    def __init__(
        self,
        func: Callable[
            [AccountLinkingUser, RecipeUserId],
            Awaitable[
                Union[
                    GetPhoneNumbersForFactorsOkResult,
                    GetPhoneNumbersForFactorsUnknownSessionRecipeUserIdResult,
                ]
            ],
        ],
    ):
        self.func = func

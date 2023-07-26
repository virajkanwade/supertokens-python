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

from typing import Any, Dict, List, Optional, Union

from supertokens_python.recipe.thirdparty.recipe import ThirdPartyRecipe

from ..types import User

from supertokens_python.recipe.multitenancy.constants import DEFAULT_TENANT_ID


async def get_user_by_id(
    user_id: str, user_context: Union[None, Dict[str, Any]] = None
) -> Union[User, None]:
    if user_context is None:
        user_context = {}
    return await ThirdPartyRecipe.get_instance().recipe_implementation.get_user_by_id(
        user_id, user_context
    )


async def get_users_by_email(
    email: str,
    tenant_id: Optional[str],
    user_context: Union[None, Dict[str, Any]] = None,
) -> List[User]:
    if user_context is None:
        user_context = {}
    return (
        await ThirdPartyRecipe.get_instance().recipe_implementation.get_users_by_email(
            email, tenant_id or DEFAULT_TENANT_ID, user_context
        )
    )


async def get_user_by_third_party_info(
    third_party_id: str,
    third_party_user_id: str,
    tenant_id: Optional[str],
    user_context: Union[None, Dict[str, Any]] = None,
):
    if user_context is None:
        user_context = {}
    return await ThirdPartyRecipe.get_instance().recipe_implementation.get_user_by_thirdparty_info(
        third_party_id,
        third_party_user_id,
        tenant_id or DEFAULT_TENANT_ID,
        user_context,
    )


async def manually_create_or_update_user(
    third_party_id: str,
    third_party_user_id: str,
    email: str,
    tenant_id: Optional[str],
    user_context: Union[None, Dict[str, Any]] = None,
):
    if user_context is None:
        user_context = {}
    return await ThirdPartyRecipe.get_instance().recipe_implementation.manually_create_or_update_user(
        third_party_id,
        third_party_user_id,
        email,
        tenant_id or DEFAULT_TENANT_ID,
        user_context,
    )


async def get_provider(
    third_party_id: str,
    client_type: Optional[str] = None,
    tenant_id: Optional[str] = None,
    user_context: Union[None, Dict[str, Any]] = None,
):
    if user_context is None:
        user_context = {}
    return await ThirdPartyRecipe.get_instance().recipe_implementation.get_provider(
        third_party_id, client_type, tenant_id or DEFAULT_TENANT_ID, user_context
    )

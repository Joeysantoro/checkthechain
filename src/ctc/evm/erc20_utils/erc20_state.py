from __future__ import annotations

import typing

from ctc import spec
from ctc import rpc

from .. import address_utils
from .. import evm_spec
from . import erc20_normalize
from . import erc20_generic


#
# # total supply
#


async def async_get_erc20_total_supply(
    token: spec.ERC20Reference,
    *,
    block: typing.Optional[spec.BlockNumberReference] = None,
    normalize: bool = True,
    provider: spec.ProviderReference = None,
    **rpc_kwargs: typing.Any,
) -> typing.Union[int, float]:
    """"""

    if block is None:
        block = 'latest'

    result = await erc20_generic.async_erc20_eth_call(
        token=token,
        function_name='totalSupply',
        block=block,
        provider=provider,
        **rpc_kwargs,
    )
    if not isinstance(result, int):
        raise Exception('invalid rpc result')
    total_supply: int | float = result

    if normalize:
        total_supply = await erc20_normalize.async_normalize_erc20_quantity(
            quantity=total_supply, token=token, provider=provider
        )

    return total_supply


async def async_get_erc20s_total_supplies(
    tokens: typing.Sequence[spec.ERC20Reference],
    *,
    block: typing.Optional[spec.BlockNumberReference] = None,
    normalize: bool = True,
    provider: spec.ProviderReference = None,
    **rpc_kwargs: typing.Any,
) -> typing.Union[list[int], list[float]]:
    """"""

    if block is None:
        block = 'latest'

    total_supplies = await erc20_generic.async_erc20s_eth_calls(
        tokens=tokens, function_name='totalSupply', block=block, **rpc_kwargs
    )

    if normalize:
        total_supplies = (
            await erc20_normalize.async_normalize_erc20s_quantities(
                tokens=tokens, quantities=total_supplies, provider=provider
            )
        )

    return total_supplies


async def async_get_erc20_total_supply_by_block(
    token: spec.ERC20Reference,
    blocks: typing.Sequence[spec.BlockNumberReference],
    *,
    normalize: bool = True,
    provider: spec.ProviderReference = None,
    **rpc_kwargs: typing.Any,
) -> typing.Union[list[int], list[float]]:

    total_supplies = await erc20_generic.async_erc20_eth_call_by_block(
        token=token,
        function_name='totalSupply',
        blocks=blocks,
        provider=provider,
        **rpc_kwargs,
    )

    if normalize:
        total_supplies = (
            await erc20_normalize.async_normalize_erc20_quantities_by_block(
                token=token,
                quantities=total_supplies,
                provider=provider,
                blocks=blocks,
            )
        )

    return total_supplies


#
# # balance of
#


async def async_get_erc20_balance_of(
    wallet: spec.Address,
    token: spec.ERC20Address,
    *,
    block: typing.Optional[spec.BlockNumberReference] = None,
    normalize: bool = True,
    provider: spec.ProviderReference = None,
    **rpc_kwargs: typing.Any,
) -> typing.Union[int, float]:

    if block is None:
        block = 'latest'

    wallet = await address_utils.async_resolve_address(
        wallet,
        block=block,
        provider=provider,
    )

    result = await erc20_generic.async_erc20_eth_call(
        token=token,
        function_name='balanceOf',
        block=block,
        function_parameters=[wallet],
        provider=provider,
        **rpc_kwargs,
    )
    if not isinstance(result, int):
        raise Exception('invalid rpc result')
    balance: int | float = result

    if normalize:
        balance = await erc20_normalize.async_normalize_erc20_quantity(
            quantity=balance, token=token, provider=provider, block=block
        )

    return balance


async def async_get_erc20_balance_of_addresses(
    wallets: typing.Sequence[spec.Address],
    token: spec.ERC20Address,
    *,
    block: typing.Optional[spec.BlockNumberReference] = None,
    normalize: bool = True,
    provider: spec.ProviderReference = None,
    **rpc_kwargs: typing.Any,
) -> typing.Union[list[int], list[float]]:

    if block is None:
        block = 'latest'

    wallets = await address_utils.async_resolve_addresses(
        wallets,
        block=block,
        provider=provider,
    )

    balances = await rpc.async_batch_eth_call(
        to_address=token,
        block_number=block,
        function_abi=evm_spec.erc20_function_abis['balanceOf'],
        function_parameter_list=[[wallet] for wallet in wallets],
        provider=provider,
        **rpc_kwargs,
    )

    if normalize:
        balances = await erc20_normalize.async_normalize_erc20_quantities(
            quantities=balances, token=token, provider=provider, block=block
        )

    return balances


async def async_get_erc20s_balance_of(
    wallet: spec.Address,
    tokens: typing.Sequence[spec.ERC20Address],
    *,
    block: typing.Optional[spec.BlockNumberReference] = None,
    normalize: bool = True,
    provider: spec.ProviderReference = None,
    **rpc_kwargs: typing.Any,
) -> typing.Union[list[int], list[float]]:
    """"""

    if block is None:
        block = 'latest'

    wallet = await address_utils.async_resolve_address(
        wallet,
        block=block,
        provider=provider,
    )

    balances = await erc20_generic.async_erc20s_eth_calls(
        tokens=tokens,
        function_name='balanceOf',
        block=block,
        function_parameters=[wallet],
        provider=provider,
        **rpc_kwargs,
    )

    if normalize:
        balances = await erc20_normalize.async_normalize_erc20s_quantities(
            quantities=balances,
            tokens=tokens,
            provider=provider,
            block=block,
        )

    return balances


async def async_get_erc20_balance_of_by_block(
    wallet: spec.Address,
    token: spec.ERC20Reference,
    *,
    blocks: typing.Sequence[spec.BlockNumberReference],
    normalize: bool = True,
    provider: spec.ProviderReference = None,
    empty_token: typing.Any = 0,
    **rpc_kwargs: typing.Any,
) -> typing.Union[list[int], list[float]]:
    """"""

    wallet = await address_utils.async_resolve_address(
        wallet,
        block=blocks[-1],
        provider=provider,
    )

    balances = await erc20_generic.async_erc20_eth_call_by_block(
        token=token,
        function_name='balanceOf',
        blocks=blocks,
        function_parameters=[wallet],
        provider=provider,
        empty_token=empty_token,
        **rpc_kwargs,
    )

    if normalize:
        balances = (
            await erc20_normalize.async_normalize_erc20_quantities_by_block(
                quantities=balances,
                token=token,
                provider=provider,
                blocks=blocks,
            )
        )

    return balances


#
# # allowance
#


async def async_get_erc20_allowance(
    token: spec.ERC20Reference,
    wallet: spec.Address,
    *,
    block: spec.BlockNumberReference | None = None,
    normalize: bool = True,
    provider: spec.ProviderReference = None,
) -> typing.Union[int, float]:

    if block is None:
        block = 'latest'

    wallet = await address_utils.async_resolve_address(
        wallet,
        block=block,
        provider=provider,
    )

    result = await erc20_generic.async_erc20_eth_call(
        token=token,
        function_name='allowance',
        block=block,
        function_parameters=[wallet],
        provider=provider,
    )
    if not isinstance(result, int):
        raise Exception('invalid rpc result')
    allowance: int | float = result

    if normalize:
        allowance = await erc20_normalize.async_normalize_erc20_quantity(
            quantity=allowance, token=token, provider=provider, block=block
        )

    return allowance


async def async_get_erc20_allowance_by_block(
    token: spec.ERC20Reference,
    wallet: spec.Address,
    *,
    blocks: typing.Sequence[spec.BlockNumberReference],
    normalize: bool = True,
    provider: spec.ProviderReference = None,
) -> typing.Union[list[int], list[float]]:

    wallet = await address_utils.async_resolve_address(
        wallet,
        block=blocks[-1],
        provider=provider,
    )

    allowances = await erc20_generic.async_erc20_eth_call_by_block(
        token=token,
        function_name='allowance',
        blocks=blocks,
        function_parameters=[wallet],
        provider=provider,
    )

    if normalize:
        allowances = (
            await erc20_normalize.async_normalize_erc20_quantities_by_block(
                quantities=allowances,
                token=token,
                provider=provider,
                blocks=blocks,
            )
        )

    return allowances


async def async_get_erc20s_allowances(
    tokens: typing.Sequence[spec.ERC20Reference],
    wallet: spec.Address,
    *,
    block: spec.BlockNumberReference | None = None,
    normalize: bool = True,
    provider: spec.ProviderReference = None,
) -> typing.Union[list[int], list[float]]:

    wallet = await address_utils.async_resolve_address(
        wallet,
        block=block,
        provider=provider,
    )

    allowances = await erc20_generic.async_erc20s_eth_calls(
        tokens=tokens,
        function_name='allowance',
        block=block,
        function_parameters=[wallet],
        provider=provider,
    )

    if normalize:
        allowances = await erc20_normalize.async_normalize_erc20s_quantities(
            quantities=allowances, tokens=tokens, provider=provider, block=block
        )

    return allowances


async def async_get_erc20s_allowances_by_address(
    token: spec.ERC20Reference,
    wallets: typing.Sequence[spec.Address],
    *,
    block: spec.BlockNumberReference | None = None,
    normalize: bool = True,
    provider: spec.ProviderReference = None,
) -> typing.Sequence[int | float]:

    wallets = await address_utils.async_resolve_addresses(
        wallets,
        block=block,
        provider=provider,
    )

    allowances = await rpc.async_batch_eth_call(
        to_address=token,
        block_number=block,
        function_abi=evm_spec.erc20_function_abis['allowance'],
        function_parameter_list=[[wallet] for wallet in wallets],
        provider=provider,
    )

    if normalize:
        allowances = await erc20_normalize.async_normalize_erc20_quantities(
            quantities=allowances, token=token, provider=provider, block=block
        )

    return allowances

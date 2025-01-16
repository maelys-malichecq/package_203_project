# Changelog

<!--next-version-placeholder-->

## v0.0.0 (12/01/2025)

- First release of `package_203_project`!


## [0.1.0]
### Added
- Initial release with six new functions useful for portfolio check: VaR, returns, volatility etc.. 
- Allow to let the client have an idea of the risks associated with its strategy.  

## [0.1.1]
### Added
- Introduced two functions for risk measurement. (but removed later)

## [0.1.2]
### Added
- User-friendly function for backtests with graph generation.
- Still in the perspective of using the backtests with clients - important to illustrate the results of the backtest as a selling argument 

## [0.1.3]
### Misc
- Version 0.1.3 released with minor updates.

## [0.1.5]
### Added
- Added new functions to `stocks_function` with corresponding tests.
- This section is created to help stock picing clients or asset managers, they can compare stocks' dynamics with a certain benchmark of their choice. 

## [0.1.7]
### Fixed
- Corrected the `modified_broker` function and verified its execution.
- Corrected directly the broker file from pybacktestchain to return a more "client friendly backtest" : graphs of the return + of weight allocation 

## [0.2.0]
### Added
- All functions are fully operational and tested.
- Test file used to test all the code added, functions run. 

## [0.2.1]
### Fixed
- Minor version release with internal fixes.

## [0.2.2]
### Added
- New function enabling users to perform a stock analysis on selected stocks. 
- Fixed beta function alignment for benchmarks (index and date mismatches).

## [0.2.3]
### Added
- Function to calculate Value at Risk (VaR), adjusted for skewness and kurtosis of backtest returns.
- Tests verified for the new feature.

## [0.2.4]
### Added
- New function to compute portfolio allocation using the maximum Sharpe ratio.
- New function to compute portfolio allocation using the equal weight portfolio. 

## [0.3.0]
### Added
- Final version tested with a new function allowing the user to choose parameters for backtests.
- Tests added in `test_package_203_project`.

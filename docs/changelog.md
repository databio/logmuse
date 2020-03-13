# Changelog

## [0.2.6] -- 2020-03-13
### Added
- Parameter in `init_logger` to use complete level names in fuller message format

### Changed
- Update testing requirements

## [0.2.5] -- 2019-11-01
### Added
- License for conda packaging

## [0.2.4] -- 2019-07-29

### Added
- New documentation

### Fixed
- Fix readme display

### Changed
- Tweak variable names

## [0.2.1] -- 2019-07-02
### Added
- Control for strictness of requirement for client code to have called `add_logging_options` when 
prior to using `logger_via_cli`
### Fixed
- Remove erroneous printing of invalid stream location message.

## [0.2.0] -- 2019-06-02

### Changed
- Deprecated `setup_logger` in favor of `init_logger`
- Changed argparser help interface to fit each arg on one line

## [0.1.0] -- 2019-04-30

### Added
- Parameter to `setup_logger` to pass argument to `style` parameter of `logging.Formatter`

## [0.0.2] -- 2019-04-14
### Changed
- Lessen level of some messages
### Fixed
- Avoid erroneous missing-option exception when adding standard logging options

## [0.0.1] -- 2019-04-09
### Fixed
- Fixed a bug preventing installation

## [0.0.0] -- 2019-04-08
- Initial release


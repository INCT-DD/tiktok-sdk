# CHANGELOG


## v1.1.6 (2024-10-22)

### Bug Fixes

* fix(deps): update dependency orjson to v3.10.9 ([`bf964f4`](https://github.com/INCT-DD/tiktok-sdk/commit/bf964f47fb901cb01b2e1c2bcb94cfae817033a1))


## v1.1.5 (2024-10-18)

### Bug Fixes

* fix(deps): update dependency rich to v13.9.2 ([`bf38e94`](https://github.com/INCT-DD/tiktok-sdk/commit/bf38e9491b2a81f372286cc23673bbc819dc7108))


## v1.1.4 (2024-10-18)

### Bug Fixes

* fix(deps): update dependency cytoolz to v1 ([`6eec5e8`](https://github.com/INCT-DD/tiktok-sdk/commit/6eec5e8ab972fed2476f816c842bb7e9d1e40af4))


## v1.1.3 (2024-10-18)

### Bug Fixes

* fix(deps): update dependency setuptools to v75.2.0 ([`cf8b72b`](https://github.com/INCT-DD/tiktok-sdk/commit/cf8b72b0147e25503dae4126ce2934461d102437))

### Chores

* chore(deps): update python-semantic-release/python-semantic-release action to v9.12.0 ([`84ab9d7`](https://github.com/INCT-DD/tiktok-sdk/commit/84ab9d746a8190f87b55fbfb7de7ed4b939e0cee))

### Unknown

* [pre-commit.ci] pre-commit autoupdate

updates:
- [github.com/pre-commit/pre-commit-hooks: v4.6.0 → v5.0.0](https://github.com/pre-commit/pre-commit-hooks/compare/v4.6.0...v5.0.0)
- [github.com/psf/black: 24.8.0 → 24.10.0](https://github.com/psf/black/compare/24.8.0...24.10.0) ([`ce63f8f`](https://github.com/INCT-DD/tiktok-sdk/commit/ce63f8fd604590881e9b893ce6096d929fdccf44))


## v1.1.2 (2024-10-03)

### Bug Fixes

* fix: include search id on video queries ([`797e0aa`](https://github.com/INCT-DD/tiktok-sdk/commit/797e0aa2bcebdbd8d2aece9577a226911be0b2c3))

### Refactoring

* refactor: change exception handler ([`e1db066`](https://github.com/INCT-DD/tiktok-sdk/commit/e1db06663903b200c850ad09b0ec47e7935247ac))


## v1.1.1 (2024-10-02)

### Bug Fixes

* fix(deps): update dependency rich to v13.9.1 ([`d146309`](https://github.com/INCT-DD/tiktok-sdk/commit/d1463093a468e02b6c2fa54f035c446fe98a91a6))

### Chores

* chore(deps): update python-semantic-release/python-semantic-release action to v9.9.0 ([`2cf1326`](https://github.com/INCT-DD/tiktok-sdk/commit/2cf132633950e248bda9f36bbc79a33606d1b302))


## v1.1.0 (2024-09-24)

### Documentation

* docs: fix docstrings ([`d2428f6`](https://github.com/INCT-DD/tiktok-sdk/commit/d2428f6e27d94a5a05f5ed2b1ec2a299cb6abaa6))

### Features

* feat: add comment downloading ([`e868d33`](https://github.com/INCT-DD/tiktok-sdk/commit/e868d33dd01fbb58637f58bce3c927439abc520a))


## v1.0.0 (2024-09-24)

### Breaking

* feat!: implement video queries ([`07529bb`](https://github.com/INCT-DD/tiktok-sdk/commit/07529bbb60609003854910ce96305a8be9c433f0))

### Bug Fixes

* fix: exception obscuring and complex logic ([`58491b6`](https://github.com/INCT-DD/tiktok-sdk/commit/58491b657770c9034d3eb65a534da7ac83396a53))

* fix: remove debugging artifacts ([`3a7073d`](https://github.com/INCT-DD/tiktok-sdk/commit/3a7073d90bb356c55a4bfa7b35338900c425c1be))

### Documentation

* docs: add video query information ([`08c7b3e`](https://github.com/INCT-DD/tiktok-sdk/commit/08c7b3e68a9514dea76fb7f73094aebc0a7d21e3))


## v0.5.0 (2024-09-23)

### Bug Fixes

* fix: constrain max_count ([`35a2974`](https://github.com/INCT-DD/tiktok-sdk/commit/35a2974e391d5e43ff9c15446184cf080f252423))

* fix: stop obscuring ValidationErrors in the common queries ([`ad8fa31`](https://github.com/INCT-DD/tiktok-sdk/commit/ad8fa31b7110c6524261d48671c4c6490a32d3b7))

* fix: exception handling on QueryClass ([`0c15b47`](https://github.com/INCT-DD/tiktok-sdk/commit/0c15b47156f7efc736b6b6ba9673f513b1067248))

### Continuous Integration

* ci: merge docs and release ([`20539c9`](https://github.com/INCT-DD/tiktok-sdk/commit/20539c9b8b7c0b099ed192f028c248176f69dd41))

### Documentation

* docs: fix inconsistencies in the Common.py class ([`c238de8`](https://github.com/INCT-DD/tiktok-sdk/commit/c238de8b5637dd011ad77aa49bacf8a2d6d54f36))

* docs: fix improper usage of capital letter L ([`8cc3559`](https://github.com/INCT-DD/tiktok-sdk/commit/8cc3559d505ef9d4049bea0a4b49a557577c65b9))

### Features

* feat: implement following and followers queries ([`0860186`](https://github.com/INCT-DD/tiktok-sdk/commit/0860186667c400ef9246c29b7301b359c0c947c6))

### Refactoring

* refactor: filter json_data to remove None values ([`3e98068`](https://github.com/INCT-DD/tiktok-sdk/commit/3e9806802adb2b30e74d6b116497ff1512ea626a))

* refactor: streamline queries ([`88f5d1b`](https://github.com/INCT-DD/tiktok-sdk/commit/88f5d1b691fb4ef8861653d4615af9839777fca6))


## v0.4.0 (2024-09-20)

### Documentation

* docs: fix module docs ([`e7bb2a9`](https://github.com/INCT-DD/tiktok-sdk/commit/e7bb2a92b44f5a7badd9fd683d197d3dbcc6b7d5))

### Features

* feat: add query for reposted videos ([`9c2c96d`](https://github.com/INCT-DD/tiktok-sdk/commit/9c2c96d2b8e6d5932cab5f5f94dd36d215207b93))


## v0.3.0 (2024-09-20)

### Documentation

* docs: fix docs after refactor ([`1c6fc94`](https://github.com/INCT-DD/tiktok-sdk/commit/1c6fc94d58f0474f2f671ab841bfca444fafa983))

### Features

* feat: add query for pinned user videos ([`e0daf63`](https://github.com/INCT-DD/tiktok-sdk/commit/e0daf63614446e4295bf8fee68d9c8e0fafc3efa))


## v0.2.2 (2024-09-18)

### Bug Fixes

* fix(deps): update dependency pydantic to v2.9.2 ([`4ab3a72`](https://github.com/INCT-DD/tiktok-sdk/commit/4ab3a7281a7f943e13e44a4d0b41f86bf2206314))


## v0.2.1 (2024-09-16)

### Bug Fixes

* fix(deps): update dependency setuptools to v75.1.0 ([`d0fe855`](https://github.com/INCT-DD/tiktok-sdk/commit/d0fe855c14ad5c0c857521fe3c5a66661023bfdf))


## v0.2.0 (2024-09-16)

### Bug Fixes

* fix(deps): update dependency setuptools to v75 (#14)

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com> ([`17e726e`](https://github.com/INCT-DD/tiktok-sdk/commit/17e726efa3db9f71bf57d4c6508c3d6da2606878))

### Continuous Integration

* ci: semantic release tags ([`0f200bf`](https://github.com/INCT-DD/tiktok-sdk/commit/0f200bf3250d43bf988148f9fc442f6b0174eb48))

### Documentation

* docs: update namespace documentation ([`f805770`](https://github.com/INCT-DD/tiktok-sdk/commit/f80577048e1322c1e4c906b1fd14c34d12d27f97))

* docs: update docstrings on relevant modules ([`dd9d97e`](https://github.com/INCT-DD/tiktok-sdk/commit/dd9d97e7ff993ea5548836f2fecb5a2d57fbbcc0))

* docs: update readme ([`392141d`](https://github.com/INCT-DD/tiktok-sdk/commit/392141d4f038466bd380c4be615336e914f31b1e))

### Features

* feat: implement query for liked videos ([`b9ed368`](https://github.com/INCT-DD/tiktok-sdk/commit/b9ed368d35d4698dfc187d35d40be23ec0ab7d56))

### Refactoring

* refactor: separate queries into their own classes ([`e272cae`](https://github.com/INCT-DD/tiktok-sdk/commit/e272caeae00a3f66bf99ddee583421b72d6275e3))


## v0.1.2 (2024-09-14)

### Bug Fixes

* fix(ci): pdoc installation ([`82c6f9d`](https://github.com/INCT-DD/tiktok-sdk/commit/82c6f9d700fbc1db30929a8b999ab94424d8d4a0))


## v0.1.1 (2024-09-14)

### Bug Fixes

* fix(ci): deps missing for doc generation ([`29db1cb`](https://github.com/INCT-DD/tiktok-sdk/commit/29db1cb802ecc03f1d17bb30afaf74fcb73e4944))

* fix(ci): install pdoc3 correctly (#12) ([`0e59cd5`](https://github.com/INCT-DD/tiktok-sdk/commit/0e59cd51e20648f2bf77fb27224aee3eb7c45dce))

### Continuous Integration

* ci: docs publishing (#11)

* refactor: change pdoc3 to docs deps group

* ci: docs publishing

* ci: call poetry lock before install ([`b105ef1`](https://github.com/INCT-DD/tiktok-sdk/commit/b105ef1bf38dc2eff1c52b9b49d5a4d60128c8b0))


## v0.1.0 (2024-09-13)

### Bug Fixes

* fix(ci): install poetry before build (#10) ([`45d3073`](https://github.com/INCT-DD/tiktok-sdk/commit/45d30734a651da46ccc5ba16052aee5e823dbf12))

* fix(deps): update dependency pydantic to v2.9.1 ([`f19d7ca`](https://github.com/INCT-DD/tiktok-sdk/commit/f19d7ca748f2d0b1ad8ee487e67c889a5fef5b36))

* fix(deps): update dependency rich to v13.8.1 ([`0e5bdcb`](https://github.com/INCT-DD/tiktok-sdk/commit/0e5bdcbda15e6f27cd8315f093f87400fcba6c33))

* fix(deps): update dependency pydantic to v2.9.0 ([`a812e3d`](https://github.com/INCT-DD/tiktok-sdk/commit/a812e3dbbe8a95105844c441857dcdf1093c7f4d))

* fix: remember dotflies are a thing ([`633772e`](https://github.com/INCT-DD/tiktok-sdk/commit/633772eea95def33c6eeb7fa76b71c116e4c4458))

* fix: change pre-commit traget branch ([`9e135a4`](https://github.com/INCT-DD/tiktok-sdk/commit/9e135a452481b70561c98d6f5dfc4fb9a98294ed))

* fix(deps): update lockfile ([`86d2294`](https://github.com/INCT-DD/tiktok-sdk/commit/86d22945f13b676fe78f60dc50a3cec1d9f9e2cc))

* fix(deps): pin dependencies ([`7d49c3a`](https://github.com/INCT-DD/tiktok-sdk/commit/7d49c3a522432fcaf750a5c93d0a82327ad11fca))

### Chores

* chore(deps): update actions/setup-python action to v5 (#9)

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com> ([`0b4ab38`](https://github.com/INCT-DD/tiktok-sdk/commit/0b4ab38951b86133b8e4c8fa4dee0fd44119d5c6))

* chore(deps): update actions/checkout action to v4 (#8)

Co-authored-by: renovate[bot] <29139614+renovate[bot]@users.noreply.github.com> ([`1617b25`](https://github.com/INCT-DD/tiktok-sdk/commit/1617b25c33508439bd142ba6a43b84b9157f6e16))

### Features

* feat(ci): add gh actions worfklow files (#7)

* feat(ci): add gh actions worfklow files

* fix(ci): try to fix detached head

* fix(ci): fix wrong branch

* fix(ci): rebase from origin

* fix(ci): add dummy git user ([`4c39926`](https://github.com/INCT-DD/tiktok-sdk/commit/4c3992619bbb92b4424d259aa2eea08aa96e0074))

* feat: add pre-commit config ([`f75f1b6`](https://github.com/INCT-DD/tiktok-sdk/commit/f75f1b65e3b2769a06674910d2a1f4dd95c65c90))

* feat: enable dependency dashboard ([`14d56ac`](https://github.com/INCT-DD/tiktok-sdk/commit/14d56ac926e71a402068f4952200e37723437268))

* feat: merge pull request #1 from INCT-DD/renovate/configure

Configure Renovate ([`f75debc`](https://github.com/INCT-DD/tiktok-sdk/commit/f75debcc8814ff0d8b080aead35ea621627bb092))

* feat: add renovate support ([`c25e635`](https://github.com/INCT-DD/tiktok-sdk/commit/c25e635d6a469fa96498ca2e9c36e173868cb88a))

### Refactoring

* refactor: change pre-commit hooks ([`4738946`](https://github.com/INCT-DD/tiktok-sdk/commit/4738946826656cd8ffb2c53a441820640e2c359e))

### Unknown

* Merge branch 'main' into renovate/configure ([`1865323`](https://github.com/INCT-DD/tiktok-sdk/commit/18653236a42530b22e35e240be674068c0d65765))

* Add renovate.json ([`42d49bb`](https://github.com/INCT-DD/tiktok-sdk/commit/42d49bb60b8ef537e792357e5a70fc7294772857))

* INITIAL COMMIT ([`25810ff`](https://github.com/INCT-DD/tiktok-sdk/commit/25810ff9f008a56666661787eb7e73b0430bfa87))

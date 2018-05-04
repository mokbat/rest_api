# REST API TEST Module
> This is a module which runs a set of test cases for performing rest api testing.

![GIT][git-image]
![DOCKER][docker-image]
![MIT][mit-license]

[mit-license]: https://img.shields.io/github/license/mashape/apistatus.svg
[git-image]: https://img.shields.io/github/release/qubyte/rubidium.svg
[docker-image]: https://img.shields.io/badge/docker-automated-green.svg
[docker-vers]: https://img.shields.io/badge/docker-18.03-blue.svg

## Installation

#### Docker
Ubuntu:

```sh
sudo apt-get install docker-ce
```

RHEL and Flavors:

```sh
sudo yum install docker-ce
```

#### GIT
Ubuntu:

```sh
sudo apt-get install git
```

RHEL and Flavors:

```sh
sudo yum install git
```

## Usage example with Docker

#### Use Git Clone, Build Docker and Run Test 
```sh
git clone https://github.com/mokbat/rest_api.git
```

## Usage example without Docker

#### Clone this repository
```sh
curl -O https://raw.githubusercontent.com/mokbat/rest_api/master/run_test.sh
```

#### Execute the script
```sh
source run_test.sh
```

#### Install dependencies for testing
```sh
pip3 install -r requirements.txt --no-index
```

#### Run Tests
```sh
python3 test_rest_api.py
```

## Meta

Your Name – Sundar Ramakrishnan – mokbat@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/mokbat/rest_api.git](https://github.com/mokbat/rest_api.git)

<!-- Markdown link & img dfn's -->
[mit-license]: https://img.shields.io/github/license/mashape/apistatus.svg
[git-image]: https://img.shields.io/github/release/qubyte/rubidium.svg
[git-vers]: https://img.shields.io/github/release/qubyte/rubidium.svg
[docker-image]: https://img.shields.io/badge/docker-automated-green.svg
[docker-vers]: https://img.shields.io/badge/docker-18.03-blue.svg

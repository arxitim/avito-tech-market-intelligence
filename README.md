# avito-tech-market-intelligence

Test job result for the Marketing intelligence department in Avito.
(https://github.com/avito-tech/mi-trainee-task)

### Launching the service
_docker-compose up_

#### The service will be deployed on the local machine.
For manual testing, you can use a URL, for example:
<br>http://127.0.0.1/generate?secret=ultra_top_secret&code_phrase=mega_code.
<br>for secret generation

<br>http://127.0.0.1/secrets/5eb97941c01262b41d6c81f9?code_phrase=mega_code
<br>to get the secret (only once!)

<b>Or you can use the FastAPI framework GUI located at http://127.0.0.1/docs</b>

### Data Storage
MongoDB is used for data storage.
This system is deployed at https://www.mongodb.com/cloud on the initial tariff plan.
Connection is made using the _pymongo_ library.
The connection scheme is described in _mongodb.py_
<br>
_The data is encrypted by the base64 mechanism_
<br>
#### TTL index set: secrets will be kept only for 10 minutes.

### Tests
Minimal tests of life activity of tests are described in _tests.py_

<details><summary><b>Coverage</b></summary>  <img src="https://github.com/arxitim/avito-tech-market-intelligence/blob/master/img/coverage.png">
</details>

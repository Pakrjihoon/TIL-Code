<h2>Airflow 설치</h2>
<hr/>

1. python 설치
2. Airflow 설치 

pip install airflow DAG정의파일과 Airflow플러그인이 저장되는 AIRFLOW_HOME 생성 AIRFLOW_HOME 환경변수 설정

3. airflow version 실행 version이 샐행되면 AIRFLOW_HOME에 airflow.cfg가 생성된다.

4. airflow db 초기화 airflow initdb 초기화하면 airflow_home에 airflow.db가 생성된다. sqlite가 default인데 sqlite의 경우 동시 액세스를 지원하지 않기 때문에 postgres나 mysql등을 고려해 보아야 한다.

5. Airflow web server start airflow webserver 8080포트로 접속해서 airflow ui 방문

<hr/>
<h2>
docker </h2>
docker-compose 설치


docker-compose에 airflow를 배포하기 위해 docker-compose.yaml을 다운
<code>curl -Lf0 'https://airflow.apache.org/docs/apache-airflow/2.1.3/docker-compose.yaml' > ./docker-compose.yaml </code>

이 파일에는 아래와 같은 서비스 정의가 포함되어 있다

- airflow-scheduler- 스케줄러 는 모든 작업과 DAG를 모니터링한 다음 종속성이 완료되면 작업 인스턴스를 트리거합니다.
- airflow-webserver- 웹서버는 http://localhost:8080.
- airflow-worker - 스케줄러에 의해 주어진 작업을 실행하는 작업자.
- airflow-init - 초기화 서비스.
- flower- 환경 모니터링을 위한 꽃 앱 . 에서 이용 가능 http://localhost:5555합니다.
- postgres - 데이터베이스.
- redis- 스케줄러에서 작업자에게 메시지를 전달하는 브로커.

환경 초기화
airflow를 처음 시작하기 전에 필요한 디렉터리를 만들고 데이터베이스를 초기화 해야한다.

<code>mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id-u)\nAIRFLOW_GID=0" > .env</code>

환경변수를 설정해준 뒤
cat .env
를 하여 제대로 할당되었는지 확인해보자
다음으로 데이터베이스를 초기화하고 계정을 생성해야 한다. 초기 계정은 airflow / airflow이다

<code>docker-compose up airflow-init</code>

<hr/>
<h2>설정초기화</h2>

설정 초기화법

<code>docker-compose down --volumes --remove-orphans docker-compose.yaml
rm -rf '<DIRECTORY>'</code>
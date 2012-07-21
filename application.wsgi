def application(environment, start_response):
    print(environment)
    print(start_response)

run(application)
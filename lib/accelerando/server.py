from optparse import OptionParser

def parse_options():
    opt_parser = OptionParser()
    opt_parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="debug or not")
    opt_parser.add_option("-D", "--daemonize", action="store_true", dest="daemonize", default=False, help="daemonize or not")
    opt_parser.add_option("-p", "--port", dest="port", metavar="PORT", default=80, help="server port")
    opt_parser.add_option("-P", "--pid", dest="pid", metavar="FILE", help="process id file")

    (options, args) = opt_parser.parse_args()

#option check logic will be here
            
    return (options, args)

def start():
    (options, args) = parse_options()
    print(options)
    
    if options.daemonize:
        daemonize()

    exec(compile(open("application.wsgi").read(), "application.wsgi", "exec"))

def daemonize():
    pass
    
def run(application):
    environment = {}
    start_response = {}
    app_iter = application(environment, start_response)

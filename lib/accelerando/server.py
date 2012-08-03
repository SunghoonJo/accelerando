from optparse import OptionParser

def parse_options():
    opt_parser = OptionParser()
    opt_parser.add_option("-a", "--application", dest="application", metavar="FILE", default="application.py", help="WSGI Application File")
    opt_parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="debug or not")
    opt_parser.add_option("-D", "--daemonize", action="store_true", dest="daemonize", default=False, help="daemonize or not")
    opt_parser.add_option("-p", "--port", dest="port", metavar="PORT", default=80, help="server port")
    opt_parser.add_option("-P", "--pid", dest="pid", metavar="FILE", help="process id file")
    
    (options, args) = opt_parser.parse_args()

    # Check invalid options


    return (options, args)

loaded_application = None

def start():
    # Check debug level

    # Check pid
    
    # Parse command-line options
    (options, args) = parse_options()

    # Load application
    load_application(options.application)
    
    APPLICATION([], [])
    # Daemonize
    if options.daemonize:
        daemonize()

    # Write pid
    if options.pid:
        write_pid(options.pid)

    # Operating System signal handling logic
    
    # Execute accelerando server


def load_application(app_filename):
    app_file = open(app_filename).read()
    exec(compile(app_file, "application.py", "exec"))    

def daemonize():
    pass    

# This function is called by application
# If application object is callable class, it may contain some application options.
# These options are configured here
# In fact, This function doesn't run application.
# The purpose of this function name is just for DSL
def run(application):
    global loaded_application
    loaded_application = application


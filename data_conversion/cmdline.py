import argparse
import os


def main():
    parser = argparse.ArgumentParser(
        description='Data-Conversion - ETL Tool used to convert data to destination style',
        usage='etl sync|async setting_file'
    )
    parser.add_argument('run_method', metavar='sync|async', type=str,
                        help='sync or async to run')
    parser.add_argument('settings_name', metavar='setting_file', type=str,
                        help='setting file name of ETL Tool')
    args = parser.parse_args()

    if args.run_method not in ['sync', 'async']:
        return 'run method must be "sync" or "async"'
    else:
        script_path = os.path.join(os.path.dirname(__file__),
                                   'run_sync.py' if args.run_method == 'sync' else
                                   'run_async.py')
        settings_path = os.path.join(os.path.abspath('.'), args.settings_name)
        if not os.path.isfile(settings_path):
            return 'please input correct settings file'
        os.system('python {script} {setting}'.format(script=script_path,
                                                     setting=settings_path))

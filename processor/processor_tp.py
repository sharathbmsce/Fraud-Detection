import traceback
import sys
import hashlib
import logging
from sawtooth_sdk.processor.handler import TransactionHandler
from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.exceptions import InternalError
from sawtooth_sdk.processor.core import TransactionProcessor

DEFAULT_URL = "tcp://validator:4004"
FAMILY_NAME = "education"
def _hash(data):
    return hashlib.sha512(data).hexdigest()

class EducationTransactionHandler(TransactionHandler):
    def __init__(self, namespace_prefix):
      
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
       
        return FAMILY_NAME
    @property
    def family_versions(self):
        
        return ['1.0']

    @property
    def namespaces(self):
       
        return [self._namespace_prefix]

    def apply(self, transaction, context):
       
        header = transaction.header
        payload_list = transaction.payload.decode().split(",")
        action = payload_list[0]
        addrs = header.inputs[0]

        if action=="add":
              self._adddata_(context, addrs,payload_list)
        
        else:
            print("unhandled")
         #   LOGGER.info("Unhandled action.")



    @classmethod
    def _adddata_(cls, context, addrs,payload_list,timeout=5):
        print("add")
        print(payload_list[1])
        state_entries=context.get_state([addrs])
        if state_entries == []:
             print("Adding")
            # LOGGER.info('Adding data %s',addrs)
             print(payload_list[1])
             state_data = (payload_list[1]+payload_list[2]).encode("utf-8")
             addresses = context.set_state({addrs: state_data})
             print("added successfully")
        else:
            raise InvalidTransaction(" exists")

def main():
    
    try:
       
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)

       
        processor = TransactionProcessor(url=DEFAULT_URL)
        sw_namespace = _hash(FAMILY_NAME.encode('utf-8'))[0:6]
        handler = EducationTransactionHandler(sw_namespace)
        processor.add_handler(handler)
        processor.start()
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()

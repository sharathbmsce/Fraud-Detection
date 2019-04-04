import hashlib
import base64
import random
import time
import requests
import yaml

from sawtooth_signing  import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch







FAMILY_NAME="education"

def _hash(data):
    return hashlib.sha512(data).hexdigest()

class EducationClient(object):
    """docstring forEducationClient."""
    def __init__(self, base_url,key_file=None):
        self._base_url=base_url

        try:
            with open(key_file) as key_fd:
                private_key_str=key_fd.read().strip()

        except OSError as err:
            raise Exception ('Failed to read  private key {} : {}'.format(key_file,str(err)))

        try:
            private_key=Secp256k1PrivateKey.from_hex(private_key_str)

        except ParseError as err:
            raise Exception('Failed to load private key:{}'.format(str(err)))
        self._signer=CryptoFactory(create_context('secp256k1'))\
        .new_signer(private_key)
        self._public_key=self._signer.get_public_key().as_hex()

    def add(self,usn,name,marks,add):
        self._address=_hash(FAMILY_NAME.encode("utf-8"))[0:6]+\
        _hash(usn.encode("utf-8"))[0:64]

        return self._wrap_and_send("add",name,marks,add,wait=10 )

    def _send_to_rest_api(self, suffix, data=None, content_type=None):
        '''Send a REST command to the Validator via the REST API.

           
        '''
        url = "{}/{}".format(self._base_url, suffix)
        print("URL to send to REST API is {}".format(url))

        headers = {}

        if content_type is not None:
            headers['Content-Type'] = content_type

        try:
            if data is not None:
                result = requests.post(url, headers=headers, data=data)
            else:
                result = requests.get(url, headers=headers)

            if not result.ok:
                raise Exception("Error {}: {}".format(
                    result.status_code, result.reason))
        except requests.ConnectionError as err:
            raise Exception(
                'Failed to connect to {}: {}'.format(url, str(err)))
        except BaseException as err:
            raise Exception(err)

        return result.text

    def _wait_for_status(self, batch_id, wait, result):
        '''Wait until transaction status is not PENDING (COMMITTED or error).

           'wait' is time to wait for status, in seconds.
        '''
        if wait and wait > 0:
            waited = 0
            start_time = time.time()
            while waited < wait:
                result = self._send_to_rest_api("batch_statuses?id={}&wait={}"
                                               .format(batch_id, wait))
                status = yaml.safe_load(result)['data'][0]['status']
                waited = time.time() - start_time

                if status != 'PENDING':
                    return result
            return "Transaction timed out after waiting {} seconds." \
               .format(wait)
        else:
            return result


    def _wrap_and_send(self, usn, name,action, wait=None):
        '''Create a transaction, then wrap it in a batch.

           Even single transactions must be wrapped into a batch.
           Called by bake() and eat().
        '''

     
        raw_payload = ",".join([action,marks, name])
        payload = raw_payload.encode() 

      
        input_and_output_address_list = [self._address]

      
        header = TransactionHeader(
            signer_public_key=self._public_key,
            family_name=FAMILY_NAME,
            family_version="1.0",
            inputs=input_and_output_address_list,
            outputs=input_and_output_address_list,
            dependencies=[],
            payload_sha512=payload,
            batcher_public_key=self._public_key,
            nonce=random.random().hex().encode()
        ).SerializeToString()

        
        transaction = Transaction(
            header=header,
            payload=payload,
            header_signature=self._signer.sign(header)
        )

        transaction_list = [transaction]

       
        header = BatchHeader(
            signer_public_key=self._public_key,
            transaction_ids=[txn.header_signature for txn in transaction_list]
        ).SerializeToString()

        
        batch = Batch(
            header=header,
            transactions=transaction_list,
            header_signature=self._signer.sign(header))

       
        batch_list = BatchList(batches=[batch])
        batch_id = batch_list.batches[0].header_signature

        
        result = self._send_to_rest_api("batches",
                                       batch_list.SerializeToString(),
                                       'application/octet-stream')

       
        return self._wait_for_status(batch_id, wait, result)

        
            
        

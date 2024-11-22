from models.request.noid_request import SchemaType
from repository.counter import CounterRepository
from utils.error_handlers import InvalidTemplateError 
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from db_config.sqlalchemy_async_connect import async_get_db
from sqlalchemy.ext.asyncio import AsyncSession
# Define character sets
DIGIT = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
XDIGIT = DIGIT + ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'n',
                 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']

# Define template types
GENTYPES = ['r', 's', 'z']
DIGTYPES = ['d', 'e']

class NoidGenerator:
    def __init__(self) -> None:
        """
        Initialize the NoidGenerator.
        """
        pass
   
    def _create_new_namespace(self,pre_prefix:str) -> str:
        """
        Create a new namespace by incrementing the numeric suffix of the previous prefix.

        Args:
            pre_prefix (str): The current prefix.

        Returns:
            str: New prefix for the namespace.

        Example: pre_prefix = m1, new+prefix = m2
        """
        if pre_prefix and pre_prefix[-1].isdigit():
            base = ''.join([c for c in pre_prefix if not c.isdigit()])
            suffix = ''.join([c for c in pre_prefix if c.isdigit()])
            new_suffix = str(int(suffix) + 1)
            new_prefix = base + new_suffix
        else:
            new_prefix = pre_prefix + '1' if pre_prefix else '1'

        return new_prefix      
    
    async def mint(self,schema:SchemaType,naan:str,session: AsyncSession, counter_instance: CounterRepository,template:str = 'reedeedeedk',) -> str:
        """
        Mint a NOID based on the provided template, scheme, and NAAN.

        Args:
            template (str): Template string for NOID generation.
            scheme (str, optional): Scheme prefix.
            naa (str, optional): NAAN (Name Assigning Authority Number).

        Returns:
            str: Generated NOID.
        """
        if '.' in template:
            prefix,mask = template.split('.',1)
        else:
            mask = template
            prefix = ''
        try:
            self.__validateMask(mask)
        except InvalidTemplateError as e:
            raise e
        
        while True:
            try:
                # Retrieve and increment the counter atomically
                n = await counter_instance.get_counter(session)
                await counter_instance.update_counter(session)
            except SQLAlchemyError as e:
                raise e
            
            noid_body = await self.__n2xdig(n,mask)
            if noid_body is not None:
                # Successfully generated NOID body
                break
            else:
                # Namespace exhausted, create a new namespace and continue
                prefix = self._create_new_namespace(prefix)
        
        noid = prefix + noid_body

        if naan:
            noid = naan + "/" + noid
        if mask[-1] == "k":
            noid += self.__checkdigit(noid)

        return noid
    
    async def __n2xdig(self,n:int,mask:str) -> Optional[str]:
        """
        Convert the counter value to a NOID body based on the mask.

        Args:
            n (int): Counter value.
            mask (str): Mask string defining the NOID format.

        Returns:
            str or None: NOID body if successful, otherwise None.
        """
        xdig = ''
        for c in mask[::-1]:
            if c == "e":
                div = len(XDIGIT)
            elif c == "d":
                div = len(DIGIT)
            else:
                continue
            value = n % div
            n = n // div
            xdig += (XDIGIT[value])
        
        if mask[0] == 'z':
            c = mask[1]
            while n > 0:
                if c == 'e':
                    div = len(XDIGIT)
                elif c == 'd':
                    div = len(DIGIT)
                else:
                    raise InvalidTemplateError("Template mask is corrupt. Cannot process character: " + c)
                value = n % div
                n = n // div
                xdig += (XDIGIT[value])

        if n > 0:
            return None
        return xdig[::-1]
    
    def __validateMask(self, mask: str) -> bool:
        """
        Validate the mask string to ensure it follows the expected format.

        Args:
            mask (str): Mask string.

        Returns:
            bool: True if valid, else raises InvalidTemplateError.
        """
        masks = ['e', 'd']
        checkchar = ['k']

        if not (mask[0] in GENTYPES or mask[0] in masks):
            raise InvalidTemplateError("Template is invalid.")
        elif not (mask[-1] in checkchar or mask[-1] in masks):
            raise InvalidTemplateError("Template is invalid.")
        else:
            for maskchar in mask[1:-1]:
                if not (maskchar in masks):
                    raise InvalidTemplateError("Template is invalid.")

        return True

    def __checkdigit(self,s:str) -> str:
        """
        Calculate and return the check digit for the NOID.

        Args:
            s (str): The NOID string without the check digit.

        Returns:
            str: The check digit character.
        """
        try:
            if s[3] == ":":
                s = s[4:].lstrip('/')
        except IndexError:
            pass

        def ordinal(x):
            try:
                return XDIGIT.index(x)
            except ValueError:
                return 0
        
        return XDIGIT[sum([x * (i+1) for i, x in enumerate(map(ordinal, s))]) % len(XDIGIT)]
        
class Encryption:
    def __init__(self):
        self.passkey = None
        self.index_to_alphabet = dict(zip(range(len('ABCDEFGHIJKLMNOPQRSTUVWXYZ')), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
        self.alphabet_to_index = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', range(len('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))))

    def set_passkey(self, key):
        if key is None:
            self.passkey = None
        else:
            self.passkey = key.upper()
    def get_passkey(self):
        return self.passkey

    def encrypt(self, plaintext):

        if self.passkey is None or len(self.passkey) == 0:
            return None

        encrypted_text = ''
        key = self.passkey
        key_index = 0

        for char in plaintext:
            if char.isalpha():
                upper_char = char.upper()
                key_char = key[key_index % len(key)]
                number = (self.alphabet_to_index[upper_char] + self.alphabet_to_index[key_char]) % 26
                cipher_char = self.index_to_alphabet[number]
                
                if char.islower():
                    cipher_char = cipher_char.lower()
                encrypted_text += cipher_char
                key_index += 1
            else:
                encrypted_text += char

        return encrypted_text
    
    def decrypt(self, encrypted_text):
        if self.passkey is None or len(self.passkey) == 0:
            return None 

        decrypted_text = ''
        key = self.passkey
        key_index = 0

        for char in encrypted_text:
            if char.isalpha():
                upper_char = char.upper()
                key_char = key[key_index % len(key)]
                number = (self.alphabet_to_index[upper_char] - self.alphabet_to_index[key_char]) % 26
                plain_char = self.index_to_alphabet[number]
                
                if char.islower():
                    plain_char = plain_char.lower()
                decrypted_text += plain_char
                key_index += 1
            else:
                decrypted_text += char

        return decrypted_text

    def handle_result(self, command, error_found = False, result = ''):
        if error_found:
            return ("ERROR Passkey not set.")
        else:
            if command in ['ENCRYPT', 'DECRYPT']:
                return (f"RESULT {result}")
            if command == 'PASS':
                return "RESULT"






def main():

    encryption = Encryption()


    while True:
        user_input = input('Enter command: ')
        user_input = user_input.strip().upper()
        user_input = user_input.split(" ", 1)


        if user_input == ['QUIT']:
            print("Exiting program.")
            break


        if len(user_input) != 2:
            print('Invalid command format, please try again.')
            continue

        command, argument = user_input

        if command in ['PASS', 'ENCRYPT', 'DECRYPT']:


            match command:
                case 'PASS':
                    encryption.set_passkey(argument)
                    print(encryption.handle_result('PASS', False if encryption.get_passkey() else True))
                    continue

                case 'ENCRYPT':
                    new_result = None

                    if encryption.get_passkey() is None:
                        new_result = encryption.handle_result('PASS', True)
                        print(new_result)
                        continue

                    result = encryption.encrypt(argument)
                    if result:
                        new_result = encryption.handle_result('ENCRYPT', False, result)
                        print(new_result)
                    continue

                case 'DECRYPT':
                    new_result = None

                    if encryption.get_passkey() is None:
                        new_result = encryption.handle_result('DECRYPT', True)
                        print(new_result)
                        continue

                    result = encryption.decrypt(argument)
                    if result:
                        new_result = encryption.handle_result('DECRYPT', False, result)
                        print(new_result)
                    continue

        else:
            print('Invalid command, please try again.')
        


    



if __name__ == "__main__":
    main()
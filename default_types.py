
def get_sanity_check(size):
    return "assert(inputData.size() >= " + size +" && \"Not enough input data!\");";
    
class SimpleType:    
    
    def get_class_declaration(self):
        declaration = []
        declaration.append("template<>")
        declaration.append("class NetworkMessage<" + self.type_name + ">")
        declaration.append("{")
        declaration.append("public:")
        declaration.append("\t" + self.get_decode_function_declaration())
        declaration.append("\t" + self.get_encode_function_declaration())
        declaration.append("};")
        
    def get_decode_function_declaration(self):
        return ["static" + self.type_name + " decode(std::vector<unsigned char> & inputData);"]
        
    def get_encode_function_declaration(self):
        return ["static std::vector<unsigned char> encode(" + self.type_name + " value);"]

    def get_decode_function_definition(self):
        definition = []
        definition.append(self.type_name + " NetworkMessage<" + self.type_name + ">::decode(std::vector<unsigned char> & inputData)")
        definition.append("{")
        definition.append("\t" + get_sanity_check(self.type_size))
        definition.append("\t" + self.type_name + " tmp = *reinterpret_cast<" + self.type_name +"*>(inputData.data());")
        definition.append("\t" + self.get_byte_ordering_decoder_line())
        definition.append("\tstd::vector<unsigned char>(inputData.begin() + " + self.type_size + ", inputData.end()).swap(inputData);")
        definition.append("\t return tmp;")
        definition.append("}")
        return definition;
 

    def get_encode_function_definition(self):
        definition = []
        definition.append("std::vector<unsigned char> NetworkMessage<" + self.type_name + ">::encode(" + self.type_name + " value)")
        definition.append("{")
        definition.append("\t" + self.get_byte_ordering_encoder_line())
        definition.append("\tconst char * tmp = reinterpret_cast<const char*>(&value);")
        definition.append("\treturn std::vector<unsigned char>(tmp, tmp + " + self.type_size +");")
        definition.append("}")
        return definition;
        
class TypeInteger(SimpleType):
    def __init__(self):
        self.type_size = "4"
        self.type_name = "int"
    
    def get_byte_ordering_decoder_line(self):
        return "tmp = static_cast<int>(ntohl(static_cast<unsigned int>(tmp)));"
    
    def get_byte_ordering_encoder_line(self):
        return "value = static_cast<int>(htonl(static_cast<unsigned int>(value)));"

class TypeUnsignedInteger(SimpleType):
    def __init__(self):
        self.type_size = "4"
        self.type_name = "unsigned int"
    
    def get_byte_ordering_decoder_line(self):
        return "tmp = static_cast<int>(ntohl(static_cast<unsigned int>(tmp)));"

    def get_byte_ordering_encoder_line(self):
        return "value = htonl(value);"
        
class TypeShort(SimpleType):
    def __init__(self):
        self.type_size = "2"
        self.type_name = "short"
    
    def get_byte_ordering_decoder_line(self):
        return "tmp = static_cast<short>(ntohs(static_cast<unsigned short>(tmp)));"
        
    def get_byte_ordering_encoder_line(self):
        return "value = static_cast<short>(htons(static_cast<unsigned short>(value)));"
        
class TypeUnsignedShort(SimpleType):
    def __init__(self):
        self.type_size = "2"
        self.type_name = "unsigned short"
    
    def get_byte_ordering_decoder_line(self):
        return "tmp = ntohs(tmp)"

    def get_byte_ordering_encoder_line(self):
        return "value = htons(value);"
        
class TypeChar(SimpleType):
    def __init__(self):
        self.type_size = "1"
        self.type_name = "char"
    
    def get_byte_ordering_decoder_line(self):
        return "" # No byte ordering for char
        
    def get_byte_ordering_encoder_line(self):
        return "" # No byte ordering for char
        
class TypeUnsignedChar(SimpleType):
    def __init__(self):
        self.type_size = "1"
        self.type_name = "unsigned char"
    
    def get_byte_ordering_decoder_line(self):
        return "" # No byte ordering for char
    
    def get_byte_ordering_encoder_line(self):
        return "" # No byte ordering for char
        
class TypeString():
    def __init__(self):
        self.type_name = "std::string"

    def get_class_declaration(self):
        declaration = []
        declaration.append("template<>")
        declaration.append("class NetworkMessage<std::string>")
        declaration.append("{")
        declaration.append("public:")
        declaration.append("\t" + self.get_decode_function_declaration())
        declaration.append("\t" + self.get_encode_function_declaration())
        declaration.append("};")
        
    def get_decode_function_declaration(self):
        return ["static std::string decode(std::vector<unsigned char> & inputData);"]

    def get_decode_function_definition(self):
        definition = []
        definition.append("std::string NetworkMessage<std::string>decode(std::vector<unsigned char> & inputData)")
        definition.append("{")
        definition.append("\tunsigned int size = decode(inputData);")
        definition.append("\t" + get_sanity_check("size"))
        definition.append("\tstd::string tmp(inputData.data(), size);")
        definition.append("\tstd::vector<unsigned char>(inputData.begin() + 4 + size, inputData.end()).swap(inputData);")
        definition.append("\t return tmp;")
        definition.append("}")
        return definition;
 
    def get_encode_function_declaration(self):
        return ["static std::vector<unsigned char> encode(const std::string & value);"]

    def get_encode_function_definition(self):
        definition = []
        definition.append("std::vector<unsigned char> NetworkMessage<std::string>::encode(const std::string & value)")
        definition.append("{")
        definition.append("\tstd::vector<unsigned char> encoded = encode(value.size());")
        definition.append("\tencoded.insert(encoded.end(), value.begin(), value.end());")
        definition.append("\treturn encoded;")
        definition.append("}")
        return definition;
        
DEFAULT_TYPES = [TypeInteger, TypeUnsignedInteger, TypeShort, TypeUnsignedShort, TypeChar, TypeUnsignedChar, TypeString]
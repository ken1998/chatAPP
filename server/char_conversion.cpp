#define BOOST_PYTHON_STATIC_LIB
#include <python/o
#include <boost/python.hpp>
#include <string>

class CharConversion{
    char[] string_to_char_list(stiring str){
        
    } 

    list char_list_to_string(char[] chars){

        
    //return list python側でarray.fromlistで追加    
    }
    

}

// モジュールの初期化ルーチン:モジュール名=char_convertion
BOOST_PYTHON_MODULE( char_convertion )
{
	// C++のstr_to_char_list関数を、str_to_charという名前でpython用に公開
	boost::python::def( "str_to_char_list", str_to_char );

	// C++のchar_list_to_strを、char_to_strという名前でpython用に公開
	boost::python::def( "char_to_str", char_list_to_str );
}
#ifndef __UUENCRYPTEASY__
#define __UUENCRYPTEASY__


typedef unsigned char		byte;
typedef int32_t             int32;

class uuEncryptEasy 
{
public:
	uuEncryptEasy():m_key ("AONESOFT"){}
	~uuEncryptEasy() {}

	virtual byte* Encrypt( byte* src , int32 length );

	virtual byte* Decrypt( byte* src , int32 length );

	void SetKey(const char* key) { m_key = key ; }

private:
	const char* m_key;
};


byte* uuEncryptEasy::Encrypt( byte* src , int32 length )
{
	int32 key_offset = 0;
	int32 key_length = strlen(m_key);
	int32 counter = 0;
	int32 src_offset = 0;

	while (src_offset < length)
	{
		while (src_offset < length && counter < 64)
		{
			src[src_offset] = src[src_offset] ^ m_key[key_offset] ;
			src_offset ++;
			key_offset = (key_offset+1) % key_length ;
			counter ++ ;
		}
		counter = 0;
		src_offset += (length/10);
	}
	return src;
}

byte* uuEncryptEasy::Decrypt( byte* src , int32 length )
{
	return Encrypt(src,length);
}
 
 #endif
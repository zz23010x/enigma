#ifdef GL_ES
  precision lowp float;
#endif

varying vec4 v_fragmentColor;
varying vec2 v_texCoord;

uniform float ofs;
uniform float dur;
uniform int hide;

uniform sampler2D tex;

void main()
{
	vec4 org = v_fragmentColor * texture2D(CC_Texture0, v_texCoord) ;

	if( hide != 0 )
	{
		gl_FragColor = org;
		return;
	}
	
	vec4 golden = dur*vec4(0.5,0.8,0.4,1.0);
	gl_FragColor =  org + texture2D(tex,vec2(v_texCoord.x, v_texCoord.y - ofs)).r*golden;
}
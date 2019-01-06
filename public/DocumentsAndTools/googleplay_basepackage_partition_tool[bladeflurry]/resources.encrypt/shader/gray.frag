
#ifdef GL_ES
  precision lowp float;
#endif

varying vec4 v_fragmentColor;
varying vec2 v_texCoord;

uniform int gray;

void main()
{
	vec4 cc = v_fragmentColor * texture2D(CC_Texture0, v_texCoord);
	if( gray>0 && cc.a > 0.0 )
		cc.r = cc.g = cc.b = dot(cc.rgb, vec3(0.299, 0.587, 0.114));
	gl_FragColor = cc;
}

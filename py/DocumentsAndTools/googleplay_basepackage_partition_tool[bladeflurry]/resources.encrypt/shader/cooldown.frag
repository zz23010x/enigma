


#ifdef GL_ES
precision lowp float;
#endif

varying vec4 v_fragmentColor;
varying vec2 v_texCoord;

uniform vec2 a;
uniform vec2 b;
uniform float percent;

void main()
{
	vec4 cc = v_fragmentColor * texture2D(CC_Texture0, v_texCoord);

	float ml = b.y - a.y;
	float cl = fract( v_texCoord ).y - a.y;

	if( (cl / ml) < 1.0 - percent)
	{
		float c = dot(cc.rgb, vec3(0.299, 0.587, 0.114));
		cc.r = cc.g = cc.b = c * 0.3;
	}

	gl_FragColor = cc;
}



#ifdef GL_ES
precision lowp float;
#endif

varying vec4 v_fragmentColor;
varying vec2 v_texCoord;

uniform vec2 a;
uniform vec2 b;

uniform bool disable;
uniform float brightness;

void main()
{
    vec4 cc = v_fragmentColor * texture2D(CC_Texture0, v_texCoord);

	if( disable )
	{
		cc.r = cc.g = cc.b = dot(cc.rgb, vec3(0.299, 0.587, 0.114));
	}
	else if( brightness > 0.1 )
	{
		float m = ( b.y - a.y ) / 2.0;
		float c = distance( ( b - a ) / 2.0 + a, fract( v_texCoord ) );

		if( c < m )
		{
			float p = c / m;
			float a = (1.0 - p)*brightness;

			vec3 rgb = cc.rgb * p + a;

			cc = vec4( rgb, cc.a );
		}
	}
	gl_FragColor = cc;
}



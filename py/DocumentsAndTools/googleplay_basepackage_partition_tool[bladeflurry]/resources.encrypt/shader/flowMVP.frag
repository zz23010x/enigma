#ifdef GL_ES
  precision lowp float;
#endif

varying vec4 v_fragmentColor;
varying vec2 v_texCoord;

uniform float offset;
uniform float light;
uniform float r;
uniform float g;
uniform float b;
uniform float a;
uniform int hide;

uniform sampler2D tex;

void main()
{
	vec4 org = v_fragmentColor * texture2D(CC_Texture0, v_texCoord);
	vec4 txc = texture2D(tex, vec2(v_texCoord.x, v_texCoord.y - offset));

	if( hide != 0 || org.a < 0.1 || txc.r < 0.02 ) {
		gl_FragColor = org;
		return;
	}

	vec3 fcl = org.rgb + a * txc.r * light * vec3( r, g, b );

	gl_FragColor = vec4( fcl, org.a );
}
uniform sampler2D u_tex01;
uniform sampler2D u_tex02;

uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;

uniform vec4 u_mat_diffuse;
uniform vec4 u_mat_specular;

uniform float u_shininess;
varying vec4 v_normal;

varying vec4 v_s;
varying vec4 v_h;
varying vec2 v_uv;

void main(void)
{

	vec4 mat_diffuse = u_mat_diffuse * texture2D(u_tex01, v_uv);
	vec4 mat_specular = u_mat_specular * texture2D(u_tex02, v_uv);

	//After finding out V, h for our global light and the normal in the vertex file. We can find find both lambert and phong from it.
	float lambertOne = max(dot(v_normal,v_s),0);
	float phongOne = max(dot(v_normal,v_h),0);

	// Lambert and phong calculations for the global light
	gl_FragColor = (lambertOne * u_light_diffuse * mat_diffuse
			  + pow(phongOne, u_shininess) * u_light_specular * mat_specular);
}
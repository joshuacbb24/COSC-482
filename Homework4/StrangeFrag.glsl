#version 330 core

/**
Strange fragment shader that colors fragments by the gl_FragCoord and some of the
GLSL buit-in functions.  The example also shows the use of functions inside a
glsl shader and using a uniform variable to control animation inside the shader.

[in] pos --- vec4 color from vertex array.
[in] color --- vec4 position from vertex array.

[out] col --- vec4 output color to the fragment shader.


*/

in vec4 pos;
in vec4 color;

out vec4 col;

uniform int shadernum = 0;
uniform float time = 0;
uniform float r = 0;
uniform float g = 0;
uniform int change = 0;


vec4 setColor1(vec4 p)
{
    return vec4(sin(p.x), cos(p.y-sin(p.x)), sin(cos(p.y) + p.x), 1);
}

vec4 setColor2(vec4 p)
{
    float x = floor(p.x) + floor(p.y);
    //int total = x;

    //vec2 ipt = vec2(x, y);
    //vec2 pt2 = vec2(p);
    //float d = distance(ipt, pt2);
    vec4 col = vec4(1, 0, 0, 1);
    vec4 col2 = vec4(0, 0, 0, 1);
    if (mod(x, 2.0) == 0)
        return col;
    else
        return col2;


}

vec4 setColor56(vec4 p)
{
    vec2 pt2 = vec2(p);
    float d = length(pt2);
    vec4 col = vec4(1, 0, 0, 1);
    return d * col;
}

vec4 setColor4(vec4 p)
{
    vec2 pt2 = vec2(p);
    float d = cos(40*length(pt2));
    float d2 = sin(40*length(pt2));
    vec4 col = vec4(1, 0, 0, 1);
    vec4 col2 = vec4(0, 1, 0, 1);
    return (d * col) + (d2 * col2);
}

vec4 setColor5(vec4 p)
{
    vec2 pt2 = vec2(p);
    float d = 0.5*(cos(10 * pt2.x)+1);
    vec4 col = vec4(0, 1, 0, 1);
    return d * col;
}

vec4 setColor6(vec4 p)
{
    vec2 pt2 = vec2(p);
    float d1 = (cos(20 * length(pt2)));
    vec4 col = d1*vec4(0, 0, 1, 1);
    return col;
}
vec4 setColor3(vec4 p)
{
    vec2 pt2 = vec2(p);
    float d = cos(40*length(pt2));
    float d2 = sin(40*length(pt2));
    float d4 = d * d2;
    float d3 = (d * d2 * d4) * 2;
    vec4 col = vec4(1, 0, 0, 1);
    vec4 col2 = vec4(0, 1, 0, 1);
    vec4 col3 = vec4(0, 0, 1, 1);
    return (d * col) + (d2 * col2) + (d4 * col3) + (d3 * col3);
}
vec4 setColor8(vec4 p)
{
    vec2 pt2 = vec2(p);
    float d = cos(50*length(pt2.x));
    float d2 = cos(50*length(pt2.y));
    vec4 col = vec4(1, 0, 0, 1);
    vec4 col2 = vec4(0, 0, 1, 1);
    return (d * col) + (d2 * col2);
}
vec4 setColor24(vec4 p)
{
    float x = floor(p.x * 5) + floor(p.y * 5);
    //int total = x;

    //vec2 ipt = vec2(x, y);
    //vec2 pt2 = vec2(p);
    //float d = distance(ipt, pt2);
    vec4 col = vec4(r, 0, 0, 1);
    vec4 col2 = vec4(0, g, 0, 1);
    if (mod(x, 2.0) == 0)
        return col;
    else
        return col2;


}
vec4 setColor25(vec4 p,vec4 l)
{
    float x = floor(p.x * 5) + floor(p.y * 5);
    //int total = x;

    //vec2 ipt = vec2(x, y);
    vec2 pt2 = vec2(l);
    //float d = distance(ipt, pt2);
    vec4 col = vec4(r, 0, 0, 1);
    vec4 col2 = vec4(0, g, 0, 1);
    float d1 = (cos(20 * length(pt2)));
    vec4 col3 = d1*vec4(0, 0, 1, 1);
    if (mod(x, 2.0) == 0)
        return col + col3;
    else
        return col2 + col3;


}
vec4 setColor26(vec4 p, vec4 l, vec4 r)
{
    vec2 pt2 = vec2(p);
    float d1 = (cos(20 * length(pt2)));
    float d2 = (sin(20 * length(l)));
    float d3 = (cos(20 * length(r.x)));
    vec4 col = d1*vec4(0, 0, 1, 1);
    vec4 col2 = d2*vec4(1, 0, 0, 1);
    vec4 col3 = d3*vec4(0, 1, 0, 1);
    return col + col2 + col3;
}
vec4 setColor27(vec4 p, vec4 l, vec4 r)
{
    vec2 pt2 = vec2(p);
    float d1 = (cos(20 * length(pt2)));
    float d2 = (sin(20 * length(l)));
    float d3 = (cos(20 * length(r)));
    vec4 col = d1*vec4(0, 0, 1, 1);
    vec4 col2 = d2*vec4(1, 0, 0, 1);
    vec4 col3 = d3*vec4(0, 1, 0, 1);
    return col + col2 + (col3);
}
void main()
{
    if (shadernum == 0)
        col = vec4(0,0,0,1);
    else if (shadernum == 1)
        col = setColor4(pos);
    else if (shadernum == 2)
        col = setColor3(pos);
    else if (shadernum == 3)
        col = setColor8(pos);
    else if (shadernum == 4)
        col = setColor2(5*pos);
    else if (shadernum == 5)
        col = setColor6(cos(length(pos)) + .1 * vec4(time, time, 0, 0));
    else if (shadernum == 6)
        col = setColor24(pos);
    else if (shadernum == 7)
        col = setColor25(pos, cos(length(pos)) + .1 * vec4(time, time, 0, 0));
    else if (shadernum == 8)
        col = setColor26(cos(length(pos)) + .1 * vec4(time, time, 0, 0), 3 * sin(length(pos)) + .1 * vec4(time, time, 0, 0), pos + .1 * vec4(time, 0, 0, 0));
    else if (shadernum == 9)
        col = setColor27(cos(length(pos)) + .2 * vec4(time, time, 0, 0), 3 * sin(length(pos)) + .2 * vec4(time, time, 0, 0), 3 * sin(length(pos)) + .5 * vec4(time, time, 0, 0));
}

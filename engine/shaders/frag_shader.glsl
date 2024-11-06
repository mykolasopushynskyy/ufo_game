#version 330 core

uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

// A single iteration of Bob Jenkins' One-At-A-Time hashing algorithm.
uint hash( uint x ) {
    x += ( x << 10u );
    x ^= ( x >>  6u );
    x += ( x <<  3u );
    x ^= ( x >> 11u );
    x += ( x << 15u );
    return x;
}

// Compound versions of the hashing algorithm I whipped together.
uint hash( uvec2 v ) { return hash( v.x ^ hash(v.y)                         ); }
uint hash( uvec3 v ) { return hash( v.x ^ hash(v.y) ^ hash(v.z)             ); }
uint hash( uvec4 v ) { return hash( v.x ^ hash(v.y) ^ hash(v.z) ^ hash(v.w) ); }

// Construct a float with half-open range [0:1] using low 23 bits.
// All zeroes yields 0.0, all ones yields the next smallest representable value below 1.0.
float floatConstruct( uint m ) {
    const uint ieeeMantissa = 0x007FFFFFu; // binary32 mantissa bitmask
    const uint ieeeOne      = 0x3F800000u; // 1.0 in IEEE binary32

    m &= ieeeMantissa;                     // Keep only mantissa bits (fractional part)
    m |= ieeeOne;                          // Add fractional part to 1.0

    float  f = uintBitsToFloat( m );       // Range [1:2]
    return f - 1.0;                        // Range [0:1]
}

// Pseudo-random value in half-open range [0:1].
float random_uniform( float x ) { return floatConstruct(hash(floatBitsToUint(x))); }
float random_uniform( vec2  v ) { return floatConstruct(hash(floatBitsToUint(v))); }
float random_uniform( vec3  v ) { return floatConstruct(hash(floatBitsToUint(v))); }
float random_uniform( vec4  v ) { return floatConstruct(hash(floatBitsToUint(v))); }

float noisy(vec3 rgb) { return rgb.r > 10 && rgb.g > 10 && rgb.b > 10 ? 1.0 : 0.0; }

float is_noisy(vec3 rgb) {
    return max(rgb.r - 100, 0.0) / (rgb.r - 100) *
           max(rgb.g - 100, 0.0) / (rgb.g - 100) *
           max(rgb.b - 100, 0.0) / (rgb.b - 100);
}

void main() {
    vec2 sample_pos = vec2(uvs.x, uvs.y);
    vec3 rgb = texture(tex, sample_pos).rgb;

    float change = random_uniform(vec3(sample_pos, time)) * 2 - 1;
    float amplitude = 0.075;

    f_color = vec4(min(rgb + is_noisy(rgb) * change * amplitude * rgb , 255.0), 1.0);
}
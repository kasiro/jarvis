// Build script for jarvis-app
// Embeds build version from environment

fn main() {
    // Pass BUILD_VERSION from environment to the code
    if let Ok(build_version) = std::env::var("BUILD_VERSION") {
        println!("cargo:rustc-env=BUILD_VERSION={}", build_version);
    }
    
    // Rebuild if git HEAD changes
    println!("cargo:rerun-if-changed=../../.git/HEAD");
}

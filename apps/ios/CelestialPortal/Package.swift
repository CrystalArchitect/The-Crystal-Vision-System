// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "CelestialPortal",
    platforms: [
        .iOS(.v17)
    ],
    dependencies: [
        // Networking
        .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.8.0"),

        // Audio (Speech-to-Text and Text-to-Speech)
        .package(url: "https://github.com/ochococo/AudioKit.git", from: "5.6.0"),

        // Local LLM inference (can be added for on-device inference)
        .package(url: "https://github.com/huggingface/swift-transformers.git", branch: "main"),

        // UI Components
        .package(url: "https://github.com/pointfreeco/swift-composable-architecture.git", from: "1.8.0"),
    ],
    targets: [
        .target(
            name: "CelestialPortal",
            dependencies: [
                "Alamofire",
                "AudioKit",
                .product(name: "ComposableArchitecture", package: "swift-composable-architecture"),
            ],
            path: "Sources"
        ),
        .testTarget(
            name: "CelestialPortalTests",
            dependencies: ["CelestialPortal"],
            path: "Tests"
        ),
    ]
)

import Foundation

public func readInput() throws -> String {
    let fileURL = Bundle.main.url(forResource: "input", withExtension: "txt")
    return try! String(contentsOf: fileURL!, encoding: String.Encoding.utf8)
}

extension String {
    public func splitlines() -> [String] {
        self.components(separatedBy: "\n")
    }
    public func split2lines() -> [String] {
        self.components(separatedBy: "\n\n")
    }
}

public func solve<I,O>(_ input: I, _ solver: (I) -> O) -> String {
    let start = Date.now
    let out = solver(input)
    let time = Date.now.timeIntervalSince(start)
    return "\(out) \(floor(time*1000))ms"
}

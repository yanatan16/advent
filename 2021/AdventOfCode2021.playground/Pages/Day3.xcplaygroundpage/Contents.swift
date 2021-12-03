//: [Previous](@previous)

import Foundation

let fileURL = Bundle.main.url(forResource: "input", withExtension: "txt")
let rawInput = try! String(contentsOf: fileURL!, encoding: String.Encoding.utf8)

let exampleRawInput = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

typealias Binary = [Int]
typealias Input = [Binary]
typealias Output = Int

func parseInput(_ inp : String) -> Input {
    inp.split(whereSeparator: \.isNewline).filter{ $0.count > 0 }.map { row in
        row.compactMap { Int(String($0)) }
    }
}

let input = parseInput(rawInput)
let example = parseInput(exampleRawInput)

func transpose<T>(_ input: [[T]]) -> [[T]] {
    input.first!.indices.map { index in
        input.map { row in row[index] }
    }
}

extension Array where Element == Int {
    func sum() -> Element {
        self.reduce(0) { return $0 + $1 }
    }
}


func binaryToInt(_ b: Binary) -> Int {
    b.reversed().enumerated().map { (index, digit) in
        //print("index \(index) digit \(digit)")
        return digit * Int(pow(2.0, Double(index)))
    }.sum()
}

//print("binary: \(binaryToInt("01001".compactMap{Int(String($0))}))")

func calcGamma(_ input: Input) -> Int {
    let binaryGamma : Binary = transpose(input).map { column in
        if column.sum() > column.count / 2 {
            return 1
        } else {
            return 0
        }
    }
    return binaryToInt(binaryGamma)
}

func calcEpsilon(_ input: Input, gamma: Int) -> Int {
    Int(pow(2.0, Double(input.first!.count))) - 1 - gamma
}

func problem1(_ input: Input) -> Output {
    let gamma = calcGamma(input)
    let epsilon = calcEpsilon(input, gamma: gamma)
    
    print("Gamma: \(gamma), Epsilon: \(epsilon)")
    return gamma * epsilon
}

func calcRating(_ input: Input, isMostCommon: Bool, position: Int) -> Int {
    let consideredValues = input.map { row in row[position] }
    let mostCommonValue = consideredValues.sum() * 2 >= input.count ? 1 : 0
    let keepValue = isMostCommon ? mostCommonValue : (1 - mostCommonValue)
    
    let filteredInput = input.filter { row in row[position] == keepValue }
    
    if filteredInput.count == 1 {
        return binaryToInt(filteredInput.first!)
    } else {
        return calcRating(filteredInput, isMostCommon: isMostCommon, position: position + 1)
    }
}

func calcRating(_ input: Input, isMostCommon: Bool) -> Int {
    calcRating(input, isMostCommon: isMostCommon, position: 0)
}

func problem2(_ input: Input) -> Output {
    let oxygen = calcRating(input, isMostCommon: true)
    let co2 = calcRating(input, isMostCommon: false)
    print("oxygen \(oxygen) co2 \(co2)")
    return oxygen * co2
}

print("Problem 1 (Example): \(problem1(example))")
print("Problem 1 (Real): \(problem1(input))")
print("Problem 2 (Example): \(problem2(example))")
print("Problem 2 (Real): \(problem2(input))")
//: [Next](@next)

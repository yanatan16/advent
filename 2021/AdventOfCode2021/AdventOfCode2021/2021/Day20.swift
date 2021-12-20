//
//  Day20.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/17/21.
//

import Foundation

struct Day20 : Solution {
    var exampleRawInput: String { """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""}
    
    typealias Algorithm = [Int]
    struct Image : CustomStringConvertible {
        let pixels: [[Int]]
        let infinitePixel: Int
        
        init(_ pixels: [[Int]], infinite: Int) {
            self.pixels = pixels
            self.infinitePixel = infinite
        }
        init(_ pixels: [[Int]]) {
            self.pixels = pixels
            self.infinitePixel = 0
        }
        
        var description: String {
            pixels.map { row in
                row.map { i in i == 1 ? "#" : "." }.joined()
            }.joined(separator: "\n")
        }
        
        var lightPixelCount: Int {
            pixels.flatMap { $0 }.sum()
        }

        func enhance(algorithm: Algorithm) -> Image {
            Image(((-1)...(pixels.count)).map { i in
                ((-1)...(pixels[0].count)).map { j in
                    let indices = [TwoDIndex(i-1,j-1), TwoDIndex(i-1,j), TwoDIndex(i-1,j+1),
                                   TwoDIndex(i,j-1), TwoDIndex(i,j), TwoDIndex(i,j+1),
                                   TwoDIndex(i+1,j-1), TwoDIndex(i+1,j), TwoDIndex(i+1,j+1)]
                    let index = BinaryDigits(indices.map { pixels.safe2DGet($0) ?? infinitePixel })
                    return algorithm[index.intRepr()]
                }
            }, infinite: infinitePixel == 1 ? algorithm.last! : algorithm.first!)
        }
    }
    struct Input {
        let algorithm: Algorithm
        let image: Image
    }
    typealias Output = Int
    
    func parsePixel(_ c: Character) -> Int {
        switch c {
        case "#":
            return 1
        default:
            return 0
        }
    }
    
    func parseInput(_ raw: String) -> Input {
        let split = raw.split2lines()
        return Input(
            algorithm: split[0].splitlines()[0].map(parsePixel),
            image: Image(split[1].splitlines().map { line in  line.map(parsePixel) })
        )
    }
    
    
    
    
    func problem1(_ input: Input) -> Int {
        // print("input: \(input)")
        
        // print("image: \(input.image)")
        let image1 = input.image.enhance(algorithm: input.algorithm)
        // print("image1: \(image1)")
        
        let image2 = image1.enhance(algorithm: input.algorithm)
        // print("image2: \(image1)")
        
        return image2.lightPixelCount
    }
    
    func problem2(_ input: Input) -> Int {
        (1...50).reduce(input.image) { (image, _) in
            image.enhance(algorithm: input.algorithm)
        }.lightPixelCount
    }
}

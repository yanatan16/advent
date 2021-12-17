//
//  Day17.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/16/21.
//

import Foundation

struct Day17 : Solution {
    var exampleRawInput: String { """
target area: x=20..30, y=-10..-5
"""}
    
    struct TargetArea {
        let xMin: Int
        let xMax: Int
        let yMin: Int
        let yMax: Int
    }
    typealias Input = TargetArea
    typealias Output = Int
    
    struct Velocity : Equatable, Hashable, CustomStringConvertible, Comparable {
        let x:Int
        let y: Int
        
        init(_ x:Int, _ y: Int) {
            self.x = x
            self.y = y
        }
        
        static func ==(l: Velocity, r: Velocity) -> Bool {
            l.x == r.x && l.y == r.y
        }
        
        static func <(l: Velocity, r: Velocity) -> Bool {
            if l.x == r.x {
                return l.y < r.y
            } else {
                return l.x < r.x
            }
        }
        
        var description: String {
            "Vel<\(x),\(y)>"
        }
    }
    
    func parseInput(_ raw: String) -> Input {
        let split = raw.splitlines()[0].components(separatedBy: "target area: ")[1].components(separatedBy: ", ")
        let xsplit = split[0].components(separatedBy: "x=")[1].components(separatedBy: "..")
        let ysplit = split[1].components(separatedBy: "y=")[1].components(separatedBy: "..")
        return TargetArea(xMin: Int(xsplit[0])!, xMax: Int(xsplit[1])!, yMin: Int(ysplit[0])!, yMax: Int(ysplit[1])!)
    }
    
    func verticalHitsTarget(_ input: Input, y: Int) -> Bool {
        var yvel = y
        if y > 0 {
            // when a positive y vel comes back down its -y - 1
            yvel = -y - 1
        }
        
        var ypos = 0
        while ypos > input.yMax {
            ypos += yvel
            yvel -= 1
        }
        
        return ypos >= input.yMin
    }
    
    func problem1(_ input: Input) -> Int {
        //        var maxDistances : [Int] = [0]
        //        for i in 1...50 {
        //            maxDistances.append(maxDistances.last! + i)
        //        }
        //        print(maxDistances.enumerated().map { ($0,$1) })
        
        //        guard let _ = maxDistances.enumerated().filter({ (x, maxX) in
        //            maxX >= input.xMin && maxX <= input.xMax
        //        }).first else {
        //            print("no valid x velocity to max out in the zone")
        //            return -1
        //        }
        
        let y = -input.yMin - 1
        
        return y * (y + 1) / 2
    }
    
    func maxSteps(_ input: Input) -> Int {
        // using logic from problem 1, the max steps is the same as the max heigh y value would take
        // Since the max y goes up, it takes 2*y to get back to the surface
        // and 1 more step to get to the target area
        
        let maxY = -input.yMin - 1
        let stepsToSurface = 2 * maxY + 1
        return stepsToSurface + 1
    }
    
    let steadyState = (0...50).map { x in x * (x + 1) / 2 }
    
    func xDistancesForSteps(_ input: Input, steps: Int) -> [Int] {
        // 1 step: x
        // 2 steps: x + (x-1) = 2x - 1
        // 3 steps: 3x - 3
        // 4: 4x - 6
        // S: S*x - S*(S-1)/2
        // given S and a target point P, calculate x = (P + S*(S-1)/2) / S
        
        // Until x just stops moving, which happens at step x
        // So we find all X that make steady state at the target area
        // and for S > min(x_steady), just return x_steady
        // steady(x) = x * (x+1) / 2 = (x^2 + x) / 2
        
        let steadyX = steadyState.enumerated().filter { (x, max) in
            max >= input.xMin && max <= input.xMax
        }.map { (x, _) in x }
        
        if steps > steadyX.min()! {
            return steadyX
        } else {
            
            let xs:[Int] = (input.xMin...input.xMax).compactMap { p in
                if (p + steps * (steps - 1) / 2) % steps == 0 {
                    return (p + steps * (steps - 1) / 2) / steps
                } else {
                    return nil
                }
            }
            
            return Set(xs).map{$0}
        }
    }
    
    func yDistancesForSteps(_ input: Input, steps: Int) -> [Int] {
        // for NEGATIVE Y
        // 1 step: y
        // 2 steps: y + (y-1) = 2y - 1
        // 3 steps: 3y - 3
        // 4: 4y - 6
        // S: S*y - S*(S-1)/2
        // given S and a target point P, calculate y = (P + S*(S-1)/2) / S
        
        let ys:[Int] = (input.yMin...input.yMax).compactMap { p in
            if (p + steps * (steps - 1) / 2) % steps == 0 {
                return (p + steps * (steps - 1) / 2) / steps
            } else {
                return nil
            }
        }
        
        return Set(ys).map{$0}
    }
    
    func problem2_original(_ input: Input) -> Int {
        print("Input: \(input)")
        
        let maxSteps = self.maxSteps(input)
        
        let startingVelocities = (1...maxSteps).flatMap { (step:Int) -> [Velocity] in
            let xs = xDistancesForSteps(input, steps: step)
            let ys = yDistancesForSteps(input, steps: step)
            
            let vels = xs.flatMap { x in
                ys.map { y in
                    Velocity(x,y)
                }
            }
            
            print("Step \(step): \(vels.sorted())")
            return vels
        }
        
        return Set(startingVelocities).count
    }
    
    func solveForVelocity(target: Int, steps: Int) -> Int? {
        if (target + steps * (steps - 1) / 2) % steps == 0 {
            return (target + steps * (steps - 1) / 2) / steps
        } else {
            return nil
        }
    }
    
    func problem2(_ input: Input) -> Int {
        let maxSteps = -2 * input.yMin
        
        let xStartingVelocitiesThatStallInTargetZone = (1...(input.xMin/2)).filter { x in
            let stallLocation = x * (x+1) / 2
            return stallLocation >= input.xMin && stallLocation <= input.xMax
        }
        
        let maxStepsToCalculateX = xStartingVelocitiesThatStallInTargetZone.min()!
        
        return (1...maxSteps).flatMap { (step:Int) -> [Velocity] in
            var xs = xStartingVelocitiesThatStallInTargetZone
            if step <= maxStepsToCalculateX {
                xs = (input.xMin...input.xMax).compactMap { solveForVelocity(target: $0, steps: step) }
            }
            let ys = (input.yMin...input.yMax).compactMap { solveForVelocity(target: $0, steps: step) }
            
            return xs.flatMap { x in ys.map { y in Velocity(x,y) } }
        }.unique().count
    }
}

//
//  ThreeD.swift
//  AdventOfCode2021
//
//  Created by Jonathan Eisen on 12/19/21.
//

import Foundation


struct ThreeDPoint : Hashable, Equatable, CustomStringConvertible {
    let x:Int, y:Int, z:Int
    typealias Magnitude = Double
    typealias Rotation = (x: Int, y: Int, z: Int)
    
    init(_ x:Int, _ y: Int, _ z: Int) {
        self.x = x
        self.y = y
        self.z = z
    }
    
    var description: String {
        "<\(x),\(y),\(z)>"
    }
    
    var magnitude: Double {
        sqrt(Double(x*x + y*y + z*z))
    }
    
    var manhattenDistance: Int {
        abs(x) + abs(y) + abs(z)
    }
    
    static func ==(l: ThreeDPoint, r: ThreeDPoint) -> Bool {
        l.x == r.x && l.y == r.y && l.z == r.z
    }
    
    static func +(_ l: ThreeDPoint, _ r: ThreeDPoint) -> ThreeDPoint {
        ThreeDPoint(l.x + r.x, l.y + r.y, l.z + r.z)
    }
    
    static prefix func -(_ n: ThreeDPoint) -> ThreeDPoint {
        ThreeDPoint(-n.x, -n.y, -n.z)
    }
    
    static func -(_ l: ThreeDPoint, _ r: ThreeDPoint) -> ThreeDPoint {
        l + (-r)
    }
    
    static func /(_ l: ThreeDPoint, _ x: Int) -> ThreeDPoint {
        ThreeDPoint(l.x/x,l.y/x,l.z/x)
    }
    
    func rotateAboutX90Degrees() -> ThreeDPoint {
        ThreeDPoint(x, z, -y)
    }
    func rotateAboutY90Degrees() -> ThreeDPoint {
        ThreeDPoint(-z, y, x)
    }
    func rotateAboutZ90Degrees() -> ThreeDPoint {
        ThreeDPoint(y, -x, z)
    }
    
    func rotate(_ x: Int, _ y: Int, _ z: Int) -> ThreeDPoint {
        var pt = self
        if (x>0) {
            (1...x).forEach { _ in pt = pt.rotateAboutX90Degrees() }
        }
        if (y>0) {
            (1...y).forEach { _ in pt = pt.rotateAboutY90Degrees() }
        }
        if (z>0) {
            (1...z).forEach { _ in pt = pt.rotateAboutZ90Degrees() }
        }
        return pt
    }
    
    func rotate(_ rot: Rotation) -> ThreeDPoint {
        rotate(rot.x, rot.y, rot.z)
    }
    
    static var allRotations : [Rotation] {
        [(0,0,0),
         (0,0,1),
         (0,0,2),
         (0,0,3),
         (0,1,0),
         (0,1,1),
         (0,1,2),
         (0,1,3),
         (0,2,0),
         (0,2,1),
         (0,2,2),
         (0,2,3),
         (0,3,0),
         (0,3,1),
         (0,3,2),
         (0,3,3),
         (1,0,0),
         (1,0,1),
         (1,0,2),
         (1,0,3),
         (1,1,0),
         (1,1,1),
         (1,1,2),
         (1,1,3),
         (1,2,0),
         (1,2,1),
         (1,2,2),
         (1,2,3),
         (1,3,0),
         (1,3,1),
         (1,3,2),
         (1,3,3),
         (2,0,0),
         (2,0,1),
         (2,0,2),
         (2,0,3),
         (2,1,0),
         (2,1,1),
         (2,1,2),
         (2,1,3),
         (2,2,0),
         (2,2,1),
         (2,2,2),
         (2,2,3),
         (2,3,0),
         (2,3,1),
         (2,3,2),
         (2,3,3),
         (3,0,0),
         (3,0,1),
         (3,0,2),
         (3,0,3),
         (3,1,0),
         (3,1,1),
         (3,1,2),
         (3,1,3),
         (3,2,0),
         (3,2,1),
         (3,2,2),
         (3,2,3),
         (3,3,0),
         (3,3,1),
         (3,3,2),
         (3,3,3)
        ]
    }
}

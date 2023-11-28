package main

import "core:mem"
import "core:math/linalg"
import "core:math/linalg/glsl"
import "core:math/cmplx"

import "core:fmt"

Matrix :: union #no_nil {
    linalg.Matrix1x1f16,
    linalg.Matrix1x1f32,
    linalg.Matrix1x1f64,
    linalg.Matrix1x2f16,
    linalg.Matrix1x2f32,
    linalg.Matrix1x2f64,
    linalg.Matrix1x3f16,
    linalg.Matrix1x3f32,
    linalg.Matrix1x3f64,
    linalg.Matrix1x4f16,
    linalg.Matrix1x4f32,
    linalg.Matrix1x4f64,
    linalg.Matrix2f16,
    linalg.Matrix2f32,
    linalg.Matrix2f64,
    linalg.Matrix2x1f16,
    linalg.Matrix2x1f32,
    linalg.Matrix2x1f64,
    linalg.Matrix2x2f16,
    linalg.Matrix2x2f32,
    linalg.Matrix2x2f64,
    linalg.Matrix2x3f16,
    linalg.Matrix2x3f32,
    linalg.Matrix2x3f64,
    linalg.Matrix2x4f16,
    linalg.Matrix2x4f32,
    linalg.Matrix2x4f64,
    linalg.Matrix3f16,
    linalg.Matrix3f32,
    linalg.Matrix3f64,
    linalg.Matrix3x1f16,
    linalg.Matrix3x1f32,
    linalg.Matrix3x1f64,
    linalg.Matrix3x2f16,
    linalg.Matrix3x2f32,
    linalg.Matrix3x2f64,
    linalg.Matrix3x3f16,
    linalg.Matrix3x3f32,
    linalg.Matrix3x3f64,
    linalg.Matrix3x4f16,
    linalg.Matrix3x4f32,
    linalg.Matrix3x4f64,
    linalg.Matrix4f16,
    linalg.Matrix4f32,
    linalg.Matrix4f64,
    linalg.Matrix4x1f16,
    linalg.Matrix4x1f32,
    linalg.Matrix4x1f64,
    linalg.Matrix4x2f16,
    linalg.Matrix4x2f32,
    linalg.Matrix4x2f64,
    linalg.Matrix4x3f16,
    linalg.Matrix4x3f32,
    linalg.Matrix4x3f64,
    linalg.Matrix4x4f16,
    linalg.Matrix4x4f32,
    linalg.Matrix4x4f64,
}

@(optimization_mode="speed")
transpose :: #force_inline proc($derived: typeid) -> Matrix {

}

@(optimization_mode="speed")
conjugate :: #force_inline proc($derived: typeid) {

}

@(optimization_mode="speed")
adjoint ::  #force_inline proc($derived: typeid) {

}

@(optimization_mode="speed")
inverse :: #force_inline proc() {

}

@(optimization_mode="speed")
trace :: #force_inline proc($derived: typeid) {

}

@(optimization_mode="speed")
det :: #force_inline proc($derived: typeid) {

}

@(optimization_mode="speed")
logdet :: proc($derived: typeid) {

}

@(optimization_mode="speed")
sum :: #force_inline proc($derived: typeid) {

}

main :: proc() {
    fmt.println("Test")
}
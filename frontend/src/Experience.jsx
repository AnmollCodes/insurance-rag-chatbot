import React, { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import * as THREE from 'three'

function Particles({ count = 200 }) {
    const mesh = useRef()

    // Create random particles
    const particles = useMemo(() => {
        const temp = []
        for (let i = 0; i < count; i++) {
            const time = Math.random() * 100
            const factor = Math.random() * 100 + 20
            const speed = Math.random() * 0.01 + 0.001
            const x = Math.random() * 20 - 10
            const y = Math.random() * 20 - 10
            const z = Math.random() * 20 - 10

            temp.push({ time, factor, speed, x, y, z })
        }
        return temp
    }, [count])

    const dummy = useMemo(() => new THREE.Object3D(), [])

    useFrame((state) => {
        if (!mesh.current) return

        particles.forEach((particle, i) => {
            let { time, factor, speed, x, y, z } = particle

            // Update time for movement
            time = particle.time += speed / 2

            // Lissajous figure-like movement
            const s = Math.cos(time)

            dummy.position.set(
                x + Math.cos((time / 10) * factor) + (Math.sin(time * 1) * factor) / 10,
                y + Math.sin((time / 10) * factor) + (Math.cos(time * 2) * factor) / 10,
                z + Math.cos((time / 10) * factor) + (Math.sin(time * 3) * factor) / 10
            )

            const scale = Math.cos(time) * 0.2 + 0.2  // Oscillating scale
            dummy.scale.set(scale, scale, scale)
            dummy.rotation.x = time
            dummy.rotation.z = time

            dummy.updateMatrix()
            mesh.current.setMatrixAt(i, dummy.matrix)
        })
        mesh.current.instanceMatrix.needsUpdate = true
    })

    return (
        <instancedMesh ref={mesh} args={[null, null, count]}>
            <dodecahedronGeometry args={[0.2, 0]} />
            <meshPhongMaterial color="#00aaff" emissive="#0000ff" wireframe={true} />
        </instancedMesh>
    )
}


export default function Experience() {
    return (
        <div id="canvas-container">
            <Canvas camera={{ position: [0, 0, 10], fov: 60 }}>
                <fog attach="fog" args={['#050505', 5, 25]} />
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} />
                <Particles count={300} />
            </Canvas>
        </div>
    )
}

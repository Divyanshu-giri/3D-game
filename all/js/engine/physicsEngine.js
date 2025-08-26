// Physics Engine - Handles physics simulation using Cannon.js
class PhysicsEngine {
    constructor() {
        this.world = null;
        this.timeStep = 1 / 60;
        this.maxSubSteps = 3;
        this.bodies = new Map();
        this.materials = new Map();
        this.contactMaterials = new Map();
        
        this.init();
    }

    init() {
        // Create physics world
        this.world = new CANNON.World();
        this.world.gravity.set(0, -9.82, 0); // Earth gravity
        this.world.broadphase = new CANNON.NaiveBroadphase();
        this.world.solver.iterations = 10;
        
        // Create default materials
        this.createDefaultMaterials();
    }

    createDefaultMaterials() {
        // Default material
        const defaultMaterial = new CANNON.Material('default');
        this.materials.set('default', defaultMaterial);
        
        // Ground material
        const groundMaterial = new CANNON.Material('ground');
        this.materials.set('ground', groundMaterial);
        
        // Player material
        const playerMaterial = new CANNON.Material('player');
        this.materials.set('player', playerMaterial);
        
        // Create contact materials
        this.createContactMaterial(defaultMaterial, defaultMaterial, 0.3, 0.0);
        this.createContactMaterial(playerMaterial, groundMaterial, 0.5, 0.0);
        this.createContactMaterial(defaultMaterial, groundMaterial, 0.4, 0.0);
    }

    createContactMaterial(mat1, mat2, friction, restitution) {
        const key = `${mat1.id}-${mat2.id}`;
        const contactMaterial = new CANNON.ContactMaterial(mat1, mat2, {
            friction: friction,
            restitution: restitution
        });
        this.world.addContactMaterial(contactMaterial);
        this.contactMaterials.set(key, contactMaterial);
    }

    createBody(options = {}) {
        const {
            type = 'box',
            position = new CANNON.Vec3(0, 0, 0),
            mass = 0,
            material = 'default',
            size = new CANNON.Vec3(1, 1, 1),
            radius = 0.5,
            height = 2,
            quaternion = new CANNON.Quaternion()
        } = options;

        let shape;

        switch (type) {
            case 'box':
                shape = new CANNON.Box(new CANNON.Vec3(size.x / 2, size.y / 2, size.z / 2));
                break;
            case 'sphere':
                shape = new CANNON.Sphere(radius);
                break;
            case 'cylinder':
                shape = new CANNON.Cylinder(radius, radius, height, 8);
                break;
            case 'plane':
                shape = new CANNON.Plane();
                break;
            default:
                shape = new CANNON.Box(new CANNON.Vec3(0.5, 0.5, 0.5));
        }

        const body = new CANNON.Body({
            mass: mass,
            material: this.materials.get(material),
            position: position,
            quaternion: quaternion
        });

        body.addShape(shape);
        this.world.addBody(body);
        this.bodies.set(body.id, body);

        return body;
    }

    removeBody(body) {
        if (this.bodies.has(body.id)) {
            this.world.removeBody(body);
            this.bodies.delete(body.id);
        }
    }

    update() {
        this.world.step(this.timeStep, this.timeStep, this.maxSubSteps);
    }

    // Raycasting for object interaction
    raycast(from, to, options = {}) {
        const raycastResult = new CANNON.RaycastResult();
        const ray = new CANNON.Ray();
        
        ray.from.copy(from);
        ray.to.copy(to);
        ray.checkCollisionResponse = options.checkCollisionResponse !== false;
        ray.collisionFilterGroup = options.collisionFilterGroup || -1;
        ray.collisionFilterMask = options.collisionFilterMask || -1;
        
        ray.intersectWorld(this.world, raycastResult);
        
        return raycastResult;
    }

    // Check if a point is inside any physics body
    isPointInsideBody(point, body) {
        const localPoint = body.pointToLocalFrame(point);
        for (const shape of body.shapes) {
            if (shape instanceof CANNON.Box) {
                const halfExtents = shape.halfExtents;
                if (Math.abs(localPoint.x) <= halfExtents.x &&
                    Math.abs(localPoint.y) <= halfExtents.y &&
                    Math.abs(localPoint.z) <= halfExtents.z) {
                    return true;
                }
            } else if (shape instanceof CANNON.Sphere) {
                if (localPoint.length() <= shape.radius) {
                    return true;
                }
            }
            // Add more shape types as needed
        }
        return false;
    }

    // Apply impulse to body
    applyImpulse(body, impulse, worldPoint) {
        if (this.bodies.has(body.id)) {
            body.applyImpulse(impulse, worldPoint);
        }
    }

    // Apply force to body
    applyForce(body, force, worldPoint) {
        if (this.bodies.has(body.id)) {
            body.applyForce(force, worldPoint);
        }
    }

    // Set body velocity
    setVelocity(body, velocity) {
        if (this.bodies.has(body.id)) {
            body.velocity.copy(velocity);
        }
    }

    // Set body angular velocity
    setAngularVelocity(body, angularVelocity) {
        if (this.bodies.has(body.id)) {
            body.angularVelocity.copy(angularVelocity);
        }
    }

    // Get all bodies in a sphere
    getBodiesInSphere(center, radius) {
        const bodiesInSphere = [];
        for (const body of this.bodies.values()) {
            const distance = body.position.distanceTo(center);
            if (distance <= radius) {
                bodiesInSphere.push(body);
            }
        }
        return bodiesInSphere;
    }

    // Get all bodies in a box
    getBodiesInBox(min, max) {
        const bodiesInBox = [];
        for (const body of this.bodies.values()) {
            const pos = body.position;
            if (pos.x >= min.x && pos.x <= max.x &&
                pos.y >= min.y && pos.y <= max.y &&
                pos.z >= min.z && pos.z <= max.z) {
                bodiesInBox.push(body);
            }
        }
        return bodiesInBox;
    }

    // Clean up
    dispose() {
        for (const body of this.bodies.values()) {
            this.world.removeBody(body);
        }
        this.bodies.clear();
        this.materials.clear();
        this.contactMaterials.clear();
        this.world = null;
    }

    // Debug methods
    enableDebug() {
        // This would connect to a visual debug renderer
        console.log('Physics debug enabled');
    }

    disableDebug() {
        console.log('Physics debug disabled');
    }
}

export { PhysicsEngine };

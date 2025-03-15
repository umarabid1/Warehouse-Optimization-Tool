window.onload = function () {
    var canvas = document.getElementById("renderCanvas");
    var engine = new BABYLON.Engine(canvas, true);
    var scene = new BABYLON.Scene(engine);

    var camera = new BABYLON.ArcRotateCamera("camera", Math.PI / 2, Math.PI / 4, 10, BABYLON.Vector3.Zero(), scene);
    camera.attachControl(canvas, true);

    var light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(0, 1, 0), scene);
    light.intensity = 1.2;

    var warehouseGround = BABYLON.MeshBuilder.CreateGround("ground", { width: 10, height: 10 }, scene);
    var groundMaterial = new BABYLON.StandardMaterial("groundMat", scene);
    groundMaterial.diffuseColor = new BABYLON.Color3(0.2, 0.2, 0.2);
    warehouseGround.material = groundMaterial;

    function createBoxes(data) {
        console.log("🔄 Creating boxes for layout:", data);

        // ✅ Remove old boxes before adding new ones
        scene.meshes.forEach(mesh => {
            if (mesh.name.startsWith("box")) {
                mesh.dispose();
            }
        });

        data.forEach((item, index) => {
            if (!item.Product_ID || !item.Aisle || !item.Shelf) {
                console.error(`❌ Missing data for item at index ${index}:`, item);
                return;
            }

            console.log(`📦 Adding Box: ${item.Product_ID} at (Aisle: ${item.Aisle}, Shelf: ${item.Shelf})`);

            var box = BABYLON.MeshBuilder.CreateBox("box" + index, { size: 0.7 }, scene);
            box.position.x = item.Aisle - 3;
            box.position.z = item.Shelf - 1.5;
            box.position.y = 0.5;

            var boxMaterial = new BABYLON.StandardMaterial("boxMat", scene);
            boxMaterial.diffuseColor = new BABYLON.Color3(0, 1, 0);
            box.material = boxMaterial;

            // ✅ Hover Information
            var advancedTexture = BABYLON.GUI.AdvancedDynamicTexture.CreateFullscreenUI("UI");
            var label = new BABYLON.GUI.TextBlock();
            label.text = `Product: ${item.Product_Name}\nID: ${item.Product_ID}\nAisle: ${item.Aisle}\nShelf: ${item.Shelf}`;
            label.color = "white";
            label.fontSize = 16;
            label.isVisible = false;
            advancedTexture.addControl(label);

            box.actionManager = new BABYLON.ActionManager(scene);
            box.actionManager.registerAction(
                new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOverTrigger, function () {
                    label.isVisible = true;
                })
            );
            box.actionManager.registerAction(
                new BABYLON.ExecuteCodeAction(BABYLON.ActionManager.OnPointerOutTrigger, function () {
                    label.isVisible = false;
                })
            );
        });
    }

    function fetchOptimizedLayout() {
        fetch("/get_optimized_layout")
            .then(response => response.json())
            .then(data => {
                console.log("✅ Optimized Layout Received:", data);
    
                if (!Array.isArray(data)) {
                    console.error("❌ Expected an array but got:", data);
                    return;
                }
    
                createBoxes(data);
            })
            .catch(error => console.error("❌ Error fetching optimized layout:", error));
    }
    

    function fetchLayouts() {
        fetch("/get_layouts")
            .then(response => response.json())
            .then(data => {
                if (data.original && data.optimized) {
                    document.getElementById("original-layout").src = "/static/warehouse_original.png?" + new Date().getTime();
                    document.getElementById("optimized-layout").src = "/static/warehouse_optimized.png?" + new Date().getTime();
                } else {
                    console.error("❌ Error: Layout data missing");
                }
            })
            .catch(error => console.error("❌ Fetch error:", error));
    }

    document.getElementById("upload-form").addEventListener("submit", function (event) {
        event.preventDefault();

        let formData = new FormData(this);

        fetch("/upload", {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                console.log("✅ Upload complete:", data.message);

                // ✅ Refresh images
                fetchLayouts();
                fetchOptimizedLayout();
            })
            .catch(error => console.error("❌ Upload error:", error));
    });

    window.addEventListener("resize", function () {
        engine.resize();
    });
};

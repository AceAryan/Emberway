"""Write Unity .meta files for generated sprite sheets and folders.

- Sprite sheets: Sprite Mode Multiple, pre-sliced into equal frames, Point filter, no compression, 32 PPU.
- IDs (GUID, internalID, spriteID) are derived from the asset path / sprite name, so they are stable.
- An existing .meta is NEVER overwritten: Unity references (animations, prefabs) depend on its GUID.
"""
import hashlib
import os

PPU = 32


def _hex(seed, n=32):
    return hashlib.md5(seed.encode("utf-8")).hexdigest()[:n]


def _internal_id(seed):
    v = int(hashlib.md5(seed.encode("utf-8")).hexdigest()[:16], 16)
    return v - (1 << 64) if v >= (1 << 63) else v   # signed 64-bit like Unity


def _rel(path, root):
    return os.path.relpath(path, root).replace("\\", "/")


def ensure_folder_meta(folder, root):
    """Create .meta files for `folder` and its parents up to Assets/."""
    folder = os.path.abspath(folder)
    assets = os.path.join(root, "Assets")
    while folder != assets and folder.startswith(assets):
        meta = folder + ".meta"
        if not os.path.exists(meta):
            with open(meta, "w", newline="\n") as f:
                f.write("fileFormatVersion: 2\n"
                        f"guid: {_hex('folder:' + _rel(folder, root))}\n"
                        "folderAsset: yes\n"
                        "DefaultImporter:\n  externalObjects: {}\n  userData: \n"
                        "  assetBundleName: \n  assetBundleVariant: \n")
            print("  meta", _rel(meta, root))
        folder = os.path.dirname(folder)


SPRITE_ENTRY = """    - serializedVersion: 2
      name: {name}
      rect:
        serializedVersion: 2
        x: {x}
        y: 0
        width: {w}
        height: {h}
      alignment: 0
      pivot: {{x: 0.5, y: 0.5}}
      border: {{x: 0, y: 0, z: 0, w: 0}}
      customData:
      outline: []
      physicsShape: []
      tessellationDetail: -1
      bones: []
      spriteID: {sid}
      internalID: {iid}
      vertices: []
      indices:
      edges: []
      weights: []
"""

PLATFORM = """  - serializedVersion: 4
    buildTarget: {target}
    maxTextureSize: 2048
    resizeAlgorithm: 0
    textureFormat: -1
    textureCompression: 0
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
    ignorePlatformSupport: 0
    androidETC2FallbackOverride: 0
    forceMaximumCompressionQuality_BC6H_BC7: 0
"""

TEXTURE_META = """fileFormatVersion: 2
guid: {guid}
TextureImporter:
  internalIDToNameTable:
{id_table}  externalObjects: {{}}
  serializedVersion: 13
  mipmaps:
    mipMapMode: 0
    enableMipMap: 0
    sRGBTexture: 1
    linearTexture: 0
    fadeOut: 0
    borderMipMap: 0
    mipMapsPreserveCoverage: 0
    alphaTestReferenceValue: 0.5
    mipMapFadeDistanceStart: 1
    mipMapFadeDistanceEnd: 3
  bumpmap:
    convertToNormalMap: 0
    externalNormalMap: 0
    heightScale: 0.25
    normalMapFilter: 0
    flipGreenChannel: 0
  isReadable: 0
  streamingMipmaps: 0
  streamingMipmapsPriority: 0
  vTOnly: 0
  ignoreMipmapLimit: 0
  grayScaleToAlpha: 0
  generateCubemap: 6
  cubemapConvolution: 0
  seamlessCubemap: 0
  textureFormat: 1
  maxTextureSize: 2048
  textureSettings:
    serializedVersion: 2
    filterMode: 0
    aniso: 1
    mipBias: 0
    wrapU: 1
    wrapV: 1
    wrapW: 1
  nPOTScale: 0
  lightmap: 0
  compressionQuality: 50
  spriteMode: 2
  spriteExtrude: 1
  spriteMeshType: 1
  alignment: 0
  spritePivot: {{x: 0.5, y: 0.5}}
  spritePixelsToUnits: {ppu}
  spriteBorder: {{x: 0, y: 0, z: 0, w: 0}}
  spriteGenerateFallbackPhysicsShape: 1
  alphaUsage: 1
  alphaIsTransparency: 1
  spriteTessellationDetail: -1
  textureType: 8
  textureShape: 1
  singleChannelComponent: 0
  flipbookRows: 1
  flipbookColumns: 1
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  ignorePngGamma: 0
  applyGammaDecoding: 0
  swizzle: 50462976
  cookieLightType: 0
  platformSettings:
{platforms}  spriteSheet:
    serializedVersion: 2
    sprites:
{sprites}    outline: []
    customData:
    physicsShape: []
    bones: []
    spriteID: {sheet_sid}
    internalID: 0
    vertices: []
    indices:
    edges: []
    weights: []
    secondaryTextures: []
    spriteCustomMetadata:
      entries: []
    nameFileIdTable:
{name_table}  mipmapLimitGroupName:
  pSDRemoveMatte: 0
  userData:
  assetBundleName:
  assetBundleVariant:
"""


def ensure_sheet_meta(png_path, frame_w, frame_h, frame_count, root):
    meta = png_path + ".meta"
    if os.path.exists(meta):
        return
    base = os.path.splitext(os.path.basename(png_path))[0]
    rel = _rel(png_path, root)
    names = [f"{base}_{i}" for i in range(frame_count)]
    ids = [_internal_id(rel + ":" + n) for n in names]
    text = TEXTURE_META.format(
        guid=_hex("asset:" + rel),
        ppu=PPU,
        id_table="".join(f"  - first:\n      213: {i}\n    second: {n}\n" for n, i in zip(names, ids)),
        platforms="".join(PLATFORM.format(target=t) for t in ("DefaultTexturePlatform", "Standalone")),
        sprites="".join(SPRITE_ENTRY.format(name=n, x=k * frame_w, w=frame_w, h=frame_h,
                                            sid=_hex("sprite:" + rel + n), iid=i)
                        for k, (n, i) in enumerate(zip(names, ids))),
        sheet_sid=_hex("sheet:" + rel),
        name_table="".join(f"      {n}: {i}\n" for n, i in zip(names, ids)),
    )
    with open(meta, "w", newline="\n") as f:
        f.write(text)
    print("  meta", _rel(meta, root))

<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0"
  xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
  xmlns="http://www.opengis.net/sld"
  xmlns:ogc="http://www.opengis.net/ogc"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  
  <NamedLayer>
    <Name>sst_colormap</Name>
    <UserStyle>
      <Name>sst_colormap</Name>
      <Title>Sea Surface Temperature Delta</Title>
      <IsDefault>1</IsDefault>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ColorMap type="ramp" extended="true">
              <ColorMapEntry color="#0000ff" quantity="0.0" label="0"/>
              <ColorMapEntry color="#00ffff" quantity="1.0" label="1"/>
              <ColorMapEntry color="#00ff00" quantity="2.0" label="2"/>
              <ColorMapEntry color="#ffff00" quantity="3.0" label="3"/>
              <ColorMapEntry color="#ff0000" quantity="4.0" label="4"/>
            </ColorMap>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>

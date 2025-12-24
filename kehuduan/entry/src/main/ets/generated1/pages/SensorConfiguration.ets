import { SensorNodeConfigurationModule } from '../view/SensorNodeConfigurationModule';
import { GlobalControlModule } from '../view/GlobalControlModule';

@Component
export struct SensorConfiguration {
  private scroller: Scroller = new Scroller();

  build() {
    Scroll(this.scroller) {
      Column() {
        SensorNodeConfigurationModule()
        GlobalControlModule()
      }
      .width('100%')
      .justifyContent(FlexAlign.Center)
      .alignItems(HorizontalAlign.Center)
    }
    .scrollable(ScrollDirection.Vertical)
    .scrollBar(BarState.Off)
    .width('100%')
    .align(Alignment.Top)
    .backgroundColor($r('app.color.page_bg_color'))
  }
}

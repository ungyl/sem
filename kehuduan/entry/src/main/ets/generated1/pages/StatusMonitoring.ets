import { ConnectionStatusModule } from '../view/ConnectionStatusModule';
import { DataTransferMonitorModule } from '../view/DataTransferMonitorModule';
import { SensorNodeStatusModule } from '../view/SensorNodeStatusModule';
import { MessageLogModule } from '../view/MessageLogModule';
import { RefreshAndConfigModule } from '../view/RefreshAndConfigModule';

@Component
export struct StatusMonitoring {
  private scroller: Scroller = new Scroller();

  build() {
    Scroll(this.scroller) {
      Column() {
        ConnectionStatusModule()
        DataTransferMonitorModule()
        SensorNodeStatusModule()
        MessageLogModule()
        RefreshAndConfigModule()
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

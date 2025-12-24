import { ServerConnectionStatusModule } from '../view/ServerConnectionStatusModule';
import { PeanutHoleConfigModule } from '../view/PeanutHoleConfigModule';
import { MessageLogHeaderModule } from '../view/MessageLogHeaderModule';
import { MessageLogCommunicationModule } from '../view/MessageLogCommunicationModule';

@Component
export struct CommunicationControl {
  private scroller: Scroller = new Scroller();

  build() {
    Scroll(this.scroller) {
      Column() {
        ServerConnectionStatusModule()
        PeanutHoleConfigModule()
        MessageLogHeaderModule()
        MessageLogCommunicationModule()
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

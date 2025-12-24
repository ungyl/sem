import { DateTimeSelectionModule } from '../view/DateTimeSelectionModule';
import { ModeToggleModule } from '../view/ModeToggleModule';
import { TimerStatusModule } from '../view/TimerStatusModule';
import { ManualQueryButtonModule } from '../view/ManualQueryButtonModule';
import { QueryResultDisplayModule } from '../view/QueryResultDisplayModule';

@Component
export struct HomePage {
  private scroller: Scroller = new Scroller();

  build() {
    Scroll(this.scroller) {
      Column() {
        DateTimeSelectionModule()
        ModeToggleModule()
        TimerStatusModule()
        ManualQueryButtonModule()
        QueryResultDisplayModule()
      }
      .width('100%')
    }
    .scrollable(ScrollDirection.Vertical)
    .scrollBar(BarState.Off)
    .width('100%')
    .height('100%')
    .align(Alignment.Top)
    .backgroundColor($r('app.color.page_bg_color'))
  }
}

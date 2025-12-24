import { EmptyPagePathStack } from './view/EmptyPagePathStack';
import { SecondPageSearch } from './view/SecondPageSearch';
import { HomePage } from './pages/HomePage';

@Entry
@Component
struct Index {
  private scroller: Scroller = new Scroller();
  @Provide('appPathStack') appPathStack: NavPathStack = new NavPathStack();
  @State title: string = 'page_title';

  @Builder
  PageMap(name: string) {
    if (name === 'SearchPage') {
      SecondPageSearch()
    } else {
      EmptyPagePathStack()
    }
  }

  build() {
    Navigation(this.appPathStack) {
      Column() {
        Scroll(this.scroller) {
          Column() {
            HomePage()
          }
          .width('100%')
          .justifyContent(FlexAlign.Start)
          .alignItems(HorizontalAlign.Start)
        }
        .scrollable(ScrollDirection.Vertical)
        .scrollBar(BarState.Off)
        .width('100%')
      }
      .backgroundColor('#F1F3F5')
      .height('100%')
    }
    .navDestination(this.PageMap)
    .hideTitleBar(true)
    .mode(NavigationMode.Stack)
  }
}
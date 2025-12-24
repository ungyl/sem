import { EmptyPagePathStack } from './view/EmptyPagePathStack';
import { SecondPageSearch } from './view/SecondPageSearch';
import { BreakpointConstants } from './common/BreakpointConstants';
import { CommonConstants } from './common/CommonConstants';
import { CommunicationControl } from './pages/CommunicationControl';
import { SensorConfiguration } from './pages/SensorConfiguration';
import { StatusMonitoring } from './pages/StatusMonitoring';

@Entry
@Component
struct Index {
  @State currentIndex: number = 0;
  private tabsController: TabsController = new TabsController();
  @Provide('appPathStack') appPathStack: NavPathStack = new NavPathStack();
  @StorageLink('currentWidthBreakpoint') currentWidthBreakpoint: string = BreakpointConstants.BREAKPOINT_SM;

  @Builder
  PageMap(name: string) {
    if (name === 'SearchPage') {
      SecondPageSearch()
    } else {
      EmptyPagePathStack()
    }
  }

  @Builder
  tabBuilder(title: string, targetIndex: number, icon: Resource) {
    Column() {
      Image(icon)
        .width("24vp")
        .height("24vp")
        .objectFit(ImageFit.Contain)
        .fillColor(this.currentIndex === targetIndex ? ($r('app.color.app_icon_pressed_color')) :
          ($r('app.color.app_icon_color')))
      Text(title)
        .fontSize("10vp")
        .fontColor(this.currentIndex === targetIndex ? ($r('app.color.app_icon_pressed_color')) :
          ($r('app.color.app_icon_color')))
        .textAlign(TextAlign.Center)
        .lineHeight("14vp")
        .fontWeight(500)
    }
    .height(this.currentWidthBreakpoint === BreakpointConstants.BREAKPOINT_LG ? "100vp" : CommonConstants.FULL_PERCENT)
    .width('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
    .onClick(() => {
      this.currentIndex = targetIndex;
      this.tabsController.changeIndex(targetIndex);
    })
  }

  build() {
    Navigation(this.appPathStack) {
      Tabs({
        barPosition: this.currentWidthBreakpoint === BreakpointConstants.BREAKPOINT_LG ? BarPosition.Start :
        BarPosition.End,
        controller: this.tabsController
      }) {
        TabContent() {
          CommunicationControl()
        }.tabBar(this.tabBuilder('通信控制', 0, $r("app.media.lib_icon_143")))

        TabContent() {
          SensorConfiguration()
        }.tabBar(this.tabBuilder('传感器配置', 1, $r("app.media.lib_icon_176")))

        TabContent() {
          StatusMonitoring()
        }.tabBar(this.tabBuilder('状态监控', 2, $r("app.media.lib_icon_3")))
      }
      .barWidth(this.currentWidthBreakpoint === BreakpointConstants.BREAKPOINT_LG ? "96vp" :
      CommonConstants.FULL_PERCENT)
      .barHeight(this.currentWidthBreakpoint === BreakpointConstants.BREAKPOINT_LG ? CommonConstants.FULL_PERCENT :
        "76vp")
      .barMode(this.currentWidthBreakpoint === BreakpointConstants.BREAKPOINT_LG ? BarMode.Scrollable : BarMode.Fixed,
        { nonScrollableLayoutStyle: LayoutStyle.ALWAYS_CENTER })
      .vertical(this.currentWidthBreakpoint === BreakpointConstants.BREAKPOINT_LG)
      .scrollable(false)
      .width('100%')
      .height('100%')
    }
    .backgroundColor($r('app.color.page_bg_color'))
    .navDestination(this.PageMap)
    .hideTitleBar(true)
    .mode(NavigationMode.Stack)
  }
}
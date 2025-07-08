import json
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from bootstrap.utils.general import make_chuncks_of_number_of_elements, list_of_dict_to_list_to_obj, GenericObject

from bootstrap.dashboard.data.store import (
    statisticsIndex1Dict,
    revenueStatDist,
    revenueProgressbarDist,
    topSellingProductsDict,
    totalSalesDonutChartWidgetDict,
    recentActivityDict,
    viewsPerMinuteDict,
    activeUsersStatDict,
    viewsPerMinuteDict,
    sessionsOsStatDict,
    channelsDict,
    socialMediaTrafficDict,
    engagementOverviewDict,
    viewsPerMinuteStatDict,
    completedTasks,
    recentActivitiesDict,
    tasksListDict,
    statisticsProjectsDict,
    totalTasks,
    yourCalendarTasksDict,
    projectStatusStatDict,
    statisticsWalletDict,
    watchList,
    moneyHistory,
    transactionList,
    statisticsDict,
    campaignsStatDict,
    revenueMonthStatDist,
    topPerformingDict,
    recentLeadsDict
)
from bootstrap.dashboard.data.charts_data import (
    projectionsVsActualsDict,
    revenueDict,
    revenueByLocationDict,
    totalSalesDonutDict,
    sessionsOverviewList,
    sessionsByCountryDict,
    sessionsOsDict,
    sessionsByBrowserDict,
    projectStatusDict,
    tasksOverviewDict,
    btc_chart_data,
    cny_chart_data,
    eth_chart_data,
    campaign_sent_data,
    new_leads_data,
    deals_data,
    booked_revenue_data,
    campaigns_data,
    revenue_data
)

User = get_user_model()


class IndexView(TemplateView):
    template_name = "bootstrap/dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        statistics_list = list_of_dict_to_list_to_obj(
            statisticsIndex1Dict)
        context['statistics'] = make_chuncks_of_number_of_elements(2, statistics_list)
        context["projectionsVsActuals"] = json.dumps(projectionsVsActualsDict)
        context['revenue_stat_data'] = GenericObject(revenueStatDist)
        context["revenue"] = json.dumps(revenueDict)
        context["revenue_by_location"] = json.dumps(revenueByLocationDict)
        context["revenue_progressbar"] = list_of_dict_to_list_to_obj(
            revenueProgressbarDist)
        context["topSellingProducts"] = list_of_dict_to_list_to_obj(
            topSellingProductsDict)
        context["totalSalesDonut"] = json.dumps(totalSalesDonutDict)
        context["totalSalesDonutChartWidget"] = list_of_dict_to_list_to_obj(
            totalSalesDonutChartWidgetDict)
        context["recentActivity"] = list_of_dict_to_list_to_obj(recentActivityDict)
        return context


index_dashboard_view = IndexView.as_view()


class DashboardAnalyticsView(TemplateView):
    template_name = "bootstrap/dashboard/analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activeUsersStat"] = GenericObject(activeUsersStatDict)
        context["viewsPerMinuteStat"] = GenericObject(viewsPerMinuteStatDict)
        context["sessionsOverview"] = json.dumps(sessionsOverviewList)
        context["sessionsByCountry"] = json.dumps(sessionsByCountryDict)
        context["viewsPerMinute"] = list_of_dict_to_list_to_obj(viewsPerMinuteDict)
        context["SessionsByBrowser"] = json.dumps(sessionsByBrowserDict)
        context["sessionsOsStat"] = GenericObject(sessionsOsStatDict)
        context["sessionsOs"] = json.dumps(sessionsOsDict)
        context["channels"] = list_of_dict_to_list_to_obj(channelsDict)
        context["socialMediaTraffic"] = list_of_dict_to_list_to_obj(socialMediaTrafficDict)
        context["engagementOverview"] = list_of_dict_to_list_to_obj(engagementOverviewDict)
        return context


analytics_dashboard_view = DashboardAnalyticsView.as_view()


class DashboardProjectsView(TemplateView):
    template_name = "bootstrap/dashboard/projects.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projectStatus"] = json.dumps(projectStatusDict)
        context["tasksOverview"] = json.dumps(tasksOverviewDict)
        context["completedTasks"] = completedTasks
        context["totalTasks"] = totalTasks
        context["projectStatusStat"] = GenericObject(projectStatusStatDict)
        context["recentActivities"] = list_of_dict_to_list_to_obj(recentActivitiesDict)
        context["tasksList"] = list_of_dict_to_list_to_obj(tasksListDict)
        context["statisticsProjects"] = GenericObject(statisticsProjectsDict)
        context["yourCalendarTasks"] = list_of_dict_to_list_to_obj(yourCalendarTasksDict)
        return context


projects_dashboard_view = DashboardProjectsView.as_view()


class DashboardCRMView(TemplateView):
    template_name = "bootstrap/dashboard/crm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statistics"] = statisticsDict
        context["campaign_stat"] = campaignsStatDict
        context['revenue_stat_data'] = GenericObject(revenueMonthStatDist)
        context["topPerforming"] = list_of_dict_to_list_to_obj(topPerformingDict)
        context["recentLeads"] = list_of_dict_to_list_to_obj(recentLeadsDict)
        context["campaign_sent_chart"] = json.dumps(campaign_sent_data)
        context["campaigns_chart"] = campaigns_data
        context["revenue_chart"] = json.dumps(revenue_data)
        context["new_leads_chart"] = new_leads_data
        context["deals_chart"] = json.dumps(deals_data)
        context["booked_revenue_chart"] = json.dumps(booked_revenue_data)
        return context


crm_dashboard_view = DashboardCRMView.as_view()


class DashboardWalletView(TemplateView):
    template_name = "bootstrap/dashboard/wallet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statistics_wallet"] = statisticsWalletDict
        context["watch_list"] = watchList
        context["money_history"] = moneyHistory
        context["transaction_list"] = transactionList
        context["btc_chart"] = btc_chart_data
        context["cny_chart"] = json.dumps(cny_chart_data)
        context["eth_chart"] = eth_chart_data
        return context


wallet_dashboard_view = DashboardWalletView.as_view()


class LoginRequiredView(TemplateView):
    pass


widgets_view = LoginRequiredView.as_view(template_name="bootstrap/dashboard/widgets.html")

# demos
demo_saas_index_dark_view = IndexView.as_view(template_name="bootstrap/demos/index-dark.html")
demo_saas_index_rtl_view = IndexView.as_view(template_name="bootstrap/demos/index-rtl.html")

demo_creative_horizontal_view = LoginRequiredView.as_view(template_name="bootstrap/demos/horizontal-creative.html")
demo_creative_horizontal_dark_view = LoginRequiredView.as_view(template_name="bootstrap/demos/horizontal-creative-dark.html")
demo_creative_horizontal_rtl_view = LoginRequiredView.as_view(template_name="bootstrap/demos/horizontal-creative-rtl.html")

demo_modern_detached_view = LoginRequiredView.as_view(template_name="bootstrap/demos/detached-modern.html")
demo_modern_detached_dark_view = LoginRequiredView.as_view(template_name="bootstrap/demos/detached-modern-dark.html")
demo_modern_detached_rtl_view = LoginRequiredView.as_view(template_name="bootstrap/demos/detached-modern-rtl.html")

demo_index_light_sidenav_layout = IndexView.as_view(template_name="bootstrap/demos/index-light-sidenav-layout.html")
demo_horizontal_boxed_layout = IndexView.as_view(template_name="bootstrap/demos/horizontal-boxed.html")

demo_full_light_layout = LoginRequiredView.as_view(template_name="bootstrap/demos/full-light.html")
demo_full_dark_layout = LoginRequiredView.as_view(template_name="bootstrap/demos/full-dark.html")
demo_full_rtl_layout = LoginRequiredView.as_view(template_name="bootstrap/demos/full-rtl.html")
